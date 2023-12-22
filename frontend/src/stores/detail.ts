import { defineStore } from "pinia";
import type { DetailData } from "@/types/Propagation/data";

export const useDetailStore = defineStore("detailView", {
  state: () => ({
    detailData: {} as DetailData,
  }),
  getters: {
    getDetailData(): DetailData {
      return this.detailData;
    },
  },
  actions: {
    setDetailData(data: DetailData) {
      this.detailData = data;
    },
  },
});
