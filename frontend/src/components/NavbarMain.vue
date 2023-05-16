<template>
  <div>
    <b-navbar toggleable="lg" type="dark" variant="info">
      <b-navbar-brand :to="{path: '/'}">
        <img src="../assets/logo.svg" alt="WooWoo" width="70%">
      </b-navbar-brand>

      <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>

      <b-collapse id="nav-collapse" is-nav>

        <b-navbar-nav class="ml-auto">
          <b-nav-form>

            <b-nav-item href="#">
              <img src="../assets/likes.svg" alt="Likes" width="70%">
            </b-nav-item>

            <b-nav-item href="#">
              <img src="../assets/chat.svg" alt="Chat" width="70%">
            </b-nav-item>

            <b-nav-item href="#">
              <img src="../assets/profile.svg" alt="Profile" width="70%">
            </b-nav-item>
          </b-nav-form>

        </b-navbar-nav>
      </b-collapse>
    </b-navbar>
  </div>
</template>

<script>
export default {
  name: "NavbarMain"
}
</script>

<style scoped>
  .bg-info {
    background-color: #B797FF !important;
  }

</style>
