<template>
  <div class="header">
    <div class="title">
      <h4>RumorVis: Interactive Analysis and Validation of Suspected Rumors on Social Media</h4>
    </div>
  </div>
</template>
<style scoped>
    .header{
      position: absolute;
      top: 0;
      height: 50px;
      width: 100%;
      min-width: 1920px;
      margin: 0 auto;
      background-color: white;
    }
    img{
      width: 50%;
      height: 50%;
      display: block;
    }
    .title{
      height: 100%;
      display: flex;
      align-items: center;
      margin-left: 20px;
    }
    h4{
      font-weight: 800;
    }
</style>
<script>
import imgURL from '../assets/img/test.png'
export default {
  data() {
    return {
      //imgUrl: imgURL,
      msg:'Hello Vue'
    }
  }
}
</script>
