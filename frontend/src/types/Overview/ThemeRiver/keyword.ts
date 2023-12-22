export type Keyword = {
  month: number;
  word: string;
  bbox?: {
    x: number;
    y: number;
    width: number;
    height: number;
  };
};

export type RawKeywordValue = {
  [key: string]: string[];
};

export type RawKeyword = {
  [key: string]: RawKeywordValue;
};
