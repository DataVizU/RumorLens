export interface TopicKeys extends Topics {
  ids: {
    [key: string]: string[];
  };
  date: string;
}

export interface Topics {
  "Current Events": number;
  "World News": number;
  Entertainment: number;
  Military: number;
  Technology: number;
  Culture: number;
  "Common Sense": number;
  "Baby Care": number;
  Education: number;
  Affection: number;
}

export type FinalData = {
  key: string;
  values: {
    date: string;
    number: number;
    ids: any;
  }[];
};
