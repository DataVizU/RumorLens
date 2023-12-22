import paddle
import paddlenlp as ppnlp
from paddlenlp.data import Stack, Pad, Tuple
import paddle.nn.functional as F
import numpy as np
import re
import random
import pandas as pd
from functools import partial  # partial()函数可以用来固定某些参数值，并返回一个新的callable对象

to_label = {
    "社会时事": "0",
    "母婴育儿": "1",
    "历史文化": "2",
    "常识": "3",
    "国际": "4",
    "军事": "5",
    "教育": "6",
    "娱乐": "7",
    "科技": "8",
    "情感": "9",
}
content = pd.read_csv("final_all_texts_nonull.csv")["content"].values.tolist()
strlabel = pd.read_csv("final_all_texts_topic_withprob_merge_nonull.csv")[
    "topic"
].values.tolist()

int_label = []
for i in range(len(content)):
    content[i] = re.sub(
        "\\【.*?\\】|\\{.*?\\}|\\<.*?\\>|\\#.*?\\#", "", content[i]
    ).replace(" ", "")
    int_label.append(to_label[strlabel[i]])

all_data = []
for i in range(len(content)):
    all_data.append([content[i], int_label[i]])

count = {
    "0": [0, []],
    "1": [0, []],
    "2": [0, []],
    "3": [0, []],
    "4": [0, []],
    "5": [0, []],
    "6": [0, []],
    "7": [0, []],
    "8": [0, []],
    "9": [0, []],
}
for i in range(len(int_label)):
    count[int_label[i]][0] += 1
    count[int_label[i]][1].append(i)

train = []
dev = []
for i in count:
    trainlen = count[i][0] // 10 * 7
    for j in range(trainlen):
        train.append(all_data[count[i][1][j]])
    for j in range(count[i][0] - trainlen):
        dev.append(all_data[count[i][1][j + trainlen]])

random.shuffle(train)
random.shuffle(dev)

trainls, devls = train[:], dev[:]
testlst = []  # 没有测试数据


class SelfDefinedDataset(paddle.io.Dataset):
    def __init__(self, data):
        super(SelfDefinedDataset, self).__init__()
        self.data = data

    def __getitem__(self, idx):
        return self.data[idx]

    def __len__(self):
        return len(self.data)

    def get_labels(self):
        return ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]


train_ds, dev_ds, test_ds = SelfDefinedDataset.get_datasets([trainls, devls, testlst])
label_list = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

print("训练集样本个数:{}".format(len(train_ds)))
print("验证集样本个数:{}".format(len(dev_ds)))
print("测试集样本个数:{}".format(len(test_ds)))

tokenizer = ppnlp.transformers.BertTokenizer.from_pretrained("bert-base-chinese")


def convert_example(example, tokenizer, label_list, max_seq_length=256, is_test=False):
    if is_test:
        text = example
    else:
        text, label = example
    # tokenizer.encode方法能够完成切分token，映射token ID以及拼接特殊token
    encoded_inputs = tokenizer.encode(text=text, max_seq_len=max_seq_length)
    input_ids = encoded_inputs["input_ids"]
    segment_ids = encoded_inputs["segment_ids"]

    if not is_test:
        label_map = {}
        for (i, l) in enumerate(label_list):
            label_map[l] = i

        label = label_map[label]
        label = np.array([label], dtype="int64")
        return input_ids, segment_ids, label
    else:
        return input_ids, segment_ids


# 数据迭代器构造方法
def create_dataloader(
    dataset,
    trans_fn=None,
    mode="train",
    batch_size=1,
    use_gpu=True,
    pad_token_id=0,
    batchify_fn=None,
):
    if trans_fn:
        dataset = dataset.apply(trans_fn, lazy=True)

    if mode == "train" and use_gpu:
        sampler = paddle.io.DistributedBatchSampler(
            dataset=dataset, batch_size=batch_size, shuffle=True
        )
    else:
        shuffle = True if mode == "train" else False  # 如果不是训练集，则不打乱顺序
        sampler = paddle.io.BatchSampler(
            dataset=dataset, batch_size=batch_size, shuffle=shuffle
        )  # 生成一个取样器
    dataloader = paddle.io.DataLoader(
        dataset, batch_sampler=sampler, return_list=True, collate_fn=batchify_fn
    )
    return dataloader


# 使用partial()来固定convert_example函数的tokenizer, label_list, max_seq_length, is_test等参数值
trans_fn = partial(
    convert_example,
    tokenizer=tokenizer,
    label_list=label_list,
    max_seq_length=128,
    is_test=False,
)
batchify_fn = lambda samples, fn=Tuple(
    Pad(axis=0, pad_val=tokenizer.pad_token_id),
    Pad(axis=0, pad_val=tokenizer.pad_token_id),
    Stack(dtype="int64"),
): [data for data in fn(samples)]
# 训练集迭代器
train_loader = create_dataloader(
    train_ds, mode="train", batch_size=64, batchify_fn=batchify_fn, trans_fn=trans_fn
)
# #验证集迭代器
dev_loader = create_dataloader(
    dev_ds, mode="dev", batch_size=64, batchify_fn=batchify_fn, trans_fn=trans_fn
)

model = ppnlp.transformers.BertForSequenceClassification.from_pretrained(
    "bert-base-chinese", num_classes=10
)

# 学习率
learning_rate = 1e-5
# 训练轮次
epochs = 100
# 学习率预热比率
warmup_proption = 0.1
# 权重衰减系数
weight_decay = 0.01

num_training_steps = len(train_loader) * epochs
num_warmup_steps = int(warmup_proption * num_training_steps)


def get_lr_factor(current_step):
    if current_step < num_warmup_steps:
        return float(current_step) / float(max(1, num_warmup_steps))
    else:
        return max(
            0.0,
            float(num_training_steps - current_step)
            / float(max(1, num_training_steps - num_warmup_steps)),
        )


# 学习率调度器
lr_scheduler = paddle.optimizer.lr.LambdaDecay(
    learning_rate, lr_lambda=lambda current_step: get_lr_factor(current_step)
)

# 优化器
optimizer = paddle.optimizer.AdamW(
    learning_rate=lr_scheduler,
    parameters=model.parameters(),
    weight_decay=weight_decay,
    apply_decay_param_fun=lambda x: x
    in [
        p.name
        for n, p in model.named_parameters()
        if not any(nd in n for nd in ["bias", "norm"])
    ],
)

# 损失函数
criterion = paddle.nn.loss.CrossEntropyLoss()
# 评估函数
metric = paddle.metric.Accuracy()

# 评估函数
def evaluate(model, criterion, metric, data_loader):
    model.eval()
    metric.reset()
    losses = []
    for batch in data_loader:
        input_ids, segment_ids, labels = batch
        logits = model(input_ids, segment_ids)
        loss = criterion(logits, labels)
        losses.append(loss.numpy())
        correct = metric.compute(logits, labels)
        metric.update(correct)
        accu = metric.accumulate()
    print("eval loss: %.5f, accu: %.5f" % (np.mean(losses), accu))
    model.train()
    metric.reset()


# 开始训练
global_step = 0
for epoch in range(1, epochs + 1):
    for step, batch in enumerate(train_loader, start=1):  # 从训练数据迭代器中取数据
        input_ids, segment_ids, labels = batch
        logits = model(input_ids, segment_ids)
        loss = criterion(logits, labels)  # 计算损失
        probs = F.softmax(logits, axis=1)
        correct = metric.compute(probs, labels)
        metric.update(correct)
        acc = metric.accumulate()

        global_step += 1
        if global_step % 50 == 0:
            print(
                "global step %d, epoch: %d, batch: %d, loss: %.5f, acc: %.5f"
                % (global_step, epoch, step, loss, acc)
            )
        loss.backward()
        optimizer.step()
        lr_scheduler.step()
        optimizer.clear_gradients()
    evaluate(model, criterion, metric, dev_loader)

model.save_pretrained("model")
tokenizer.save_pretrained("tokenzier")


def predict(model, data, tokenizer, label_map, batch_size=1):
    examples = []
    for text in data:
        input_ids, segment_ids = convert_example(
            text,
            tokenizer,
            label_list=label_map.values(),
            max_seq_length=128,
            is_test=True,
        )
        examples.append((input_ids, segment_ids))

    batchify_fn = lambda samples, fn=Tuple(
        Pad(axis=0, pad_val=tokenizer.pad_token_id),
        Pad(axis=0, pad_val=tokenizer.pad_token_id),
    ): fn(samples)
    batches = []
    one_batch = []
    for example in examples:
        one_batch.append(example)
        if len(one_batch) == batch_size:
            batches.append(one_batch)
            one_batch = []
    if one_batch:
        batches.append(one_batch)

    results = []
    model.eval()
    for batch in batches:
        input_ids, segment_ids = batchify_fn(batch)
        input_ids = paddle.to_tensor(input_ids)
        segment_ids = paddle.to_tensor(segment_ids)
        logits = model(input_ids, segment_ids)
        probs = F.softmax(logits, axis=1)
        idx = paddle.argmax(probs, axis=1).numpy()
        idx = idx.tolist()
        labels = [label_map[i] for i in idx]
        results.extend(labels)
    return results


data = [i[0] for i in dev]
label_map = {
    0: "0",
    1: "1",
    2: "2",
    3: "3",
    4: "4",
    5: "5",
    6: "6",
    7: "7",
    8: "8",
    9: "9",
}

predictions = predict(model, data, tokenizer, label_map, batch_size=32)
