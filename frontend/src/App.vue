<template>
  <div id="app">
    <NavbarMain />
    <router-view />
  </div>
</template>

<script>
  import NavbarMain from "@/components/NavbarMain.vue";

  export default {
    name: "App",
    components: {
      NavbarMain
    }
  }
</script>

<style>
  .containerAlignmentAuth {
    height: 100%;
    align-content: center;
    padding-top: 10%;
  }

  .cardHeader {
    color: #6724FF;
    /*background-color: #B797FF;*/

    text-align: center;
    font-size: 20px;
  }

  .cardFooter {
    color: #6724FF;
    /*background-color: #B797FF;*/
  }

  .card {
    background: #F8F5FD !important;
    border: 3px solid rgba(103, 36, 255, 0.64) !important;
    border-radius: 37px !important;
  }

  .btn.btn-primary {
    background-color: #B797FF !important;
  }

</style>