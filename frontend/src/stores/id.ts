import { ref } from "vue";
import { defineStore } from "pinia";

export const useIdStore = defineStore("id", () => {
  const idArrMap = ref<string[]>();
  const idArrRiver = ref<string[]>();
  const idTree = ref<string>();
  const setIdArrMap = (arr: string[]) => {
    idArrMap.value = arr;
  };
  const setIdArrRiver = (arr: string[]) => {
    idArrRiver.value = arr;
  };
  const setIdTree = (id: string) => {
    idTree.value = id;
  };
  return {
    idArrMap,
    setIdArrMap,
    idArrRiver,
    setIdArrRiver,
    idTree,
    setIdTree,
  };
});
