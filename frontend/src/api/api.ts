import http from "@/api/http";

export const getMapData = () => {
  return http.get("/overview/map2time");
};

export const getTopicData = () => {
  return http.get("/overview/time2topic");
};

export const sendRiverKeywords = (keywords: string[]) => {
  return http.post("/overview/theme-river", keywords);
};

export const getMiddleData = (ids: string[]) => {
  return http.post("/middle", ids);
};

export const setTreeMap = (id: string) => {
  return http.get(`/treemap/${id}`);
};
