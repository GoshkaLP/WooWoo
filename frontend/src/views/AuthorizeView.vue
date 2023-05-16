<template>
  <div class="container containerAlignmentAuth">
    <div class="d-flex justify-content-center h-100">
      <b-card class="authCard">
        <b-card-header class="cardHeader">
          <p>Авторизация</p>
        </b-card-header>
        <b-card-body>
          <b-form @submit="onSubmit">

            <b-form-group
                id="input-group-1"
                label="Электронная почта:"
                label-for="input-1">
              <b-form-input
                  id="input-1"
                  v-model="form.email"
                  type="email"
                  placeholder="Введите вашу почту"
                  required
              ></b-form-input>
            </b-form-group>

            <b-form-group id="input-group-2" label="Пароль:" label-for="input-2">
              <b-form-input
                  id="input-2"
                  :state="passwordState"
                  v-model="form.password"
                  type="password"
                  placeholder="Введите пароль"
                  required
              ></b-form-input>
              <b-form-invalid-feedback id="input-2-feedback">
                {{passwordMessage}}
              </b-form-invalid-feedback>
            </b-form-group>

            <b-button type="submit" variant="primary">АВТОРИЗОВАТЬСЯ</b-button>
          </b-form>
        </b-card-body>
        <b-card-footer class="cardFooter">
          <div class="d-flex justify-content-center links">
            Нет аккаунта? <router-link to="/register">Регистрация</router-link>
          </div>
        </b-card-footer>
      </b-card>
    </div>
  </div>
</template>

<script>
import {mapActions, mapGetters, mapMutations} from "vuex";

export default {
  name: "AuthorizeView",
  computed: {
    passwordState() {
      return this.getAuthForm().state;
    },
    passwordMessage() {
      return this.getAuthForm().message;
    }
  },
  data() {
    return {
      form: {
        email: '',
        password: ''
      }
    }
  },
  methods: {
    ...mapActions(["authUser"]),
    ...mapGetters(["getLoggedIn", "getAuthForm"]),
    ...mapMutations(["setAuthForm"]),

    async onSubmit(event) {
      event.preventDefault();
      let authData = new FormData();
      authData.append("email", this.form.email);
      authData.append("password", this.form.password);
      await this.authUser(authData);

      if (this.getLoggedIn()) {
        this.setAuthForm({
          state: null,
          message: ""
        });
        await this.$router.push('/');
      }
    }
  }
}
</script>

<style scoped>
  .authCard {
    font-weight: 500;
    width: 500px;
  }

</style>