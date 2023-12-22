import { ref } from "vue";
import { defineStore } from "pinia";
export const useIdStore = defineStore("id", () => {
  const idArrMap = ref();
  const idArrRiver = ref();
  const idTree = ref();
  const setIdArrMap = (arr) => {
    idArrMap.value = arr;
  };
  const setIdArrRiver = (arr) => {
    idArrRiver.value = arr;
  };
  const setIdTree = (id) => {
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
