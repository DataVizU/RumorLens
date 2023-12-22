export type NewData = {
  [key: string]: {
    date: string;
    topic: Topic[];
  };
};

type Topic = {
  name: string;
  num: number;
  id: string[];
};
