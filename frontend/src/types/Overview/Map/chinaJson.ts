export type ChinaJson = {
  type: string;
  features: Feature[];
};

export type Feature =
  | {
      type: string;
      properties: {
        adcode: number;
        name: string;
        center: number[];
        centroid: number[];
        childrenNum: number;
        level: string;
        parent: { adcode: number };
        subFeatureIndex: number;
        acroutes: number[];
        adchar?: undefined;
      };
      geometry: {};
    }
  | {};
// 给加上类型会报错...
