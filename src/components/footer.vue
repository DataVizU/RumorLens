<template>
    <!-- <footer class="fixed-bottom clearfix">
       <div class="col3">
          <router-link to="/index">index</router-link>
        </div>
    </footer>-->
  <footer id="copyright">©️2021</footer>
</template>
<script>
    export default{
        data(){
            return{
                msg: ''
            }
        }
    }
</script>
<style scoped>
    footer{
      width:100%;
      min-width: 1920px;
      height:30px;
      bottom:0;
      position: absolute;
      line-height: 30px;
      text-align:center;
      background-color: white;
    }
</style>
