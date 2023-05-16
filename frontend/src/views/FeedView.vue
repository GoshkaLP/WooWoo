<template>
  <div>
    <div class="container containerAlignmentForm" v-if="currentUser !== -1 && getUserFeed.data.length !== 0 && getUserFeed.loaded">
      <div class="d-flex justify-content-center h-100">
          <b-card class="userFormCard">

            <b-container>
              <b-row class="align-items-center">
                <b-col class="dislike" @click="dislikeButton">
                  <img src="../assets/dislike.svg" alt="dislike">
                </b-col>
                <b-col>
                  <b-card class="userPhotoCard">
                    <img
                        class="userPhoto"
                        alt="user_photo"
                        v-bind:src="'data:image/jpeg;base64,'+getCurrentUser.photo"
                        />
                  </b-card>
                </b-col>
                <b-col class="like" @click="likeButton">
                  <img src="../assets/like.svg" alt="like">
                </b-col>
              </b-row>
            </b-container>


            <b-card-text class="userFormNameAge">
              {{getUserFeed.data[currentUser].name}} {{getUserFeed.data[currentUser].surname}}
            </b-card-text>

            <b-container>
              <b-row сlass="align-items-center">
                <b-col v-for="interest in getCurrentUser.interests" :key="interest.id">
                    <b-card class="interest">
                      <b-card-text class="interestTitle">{{interest.interest_title}}</b-card-text>
                    </b-card>
                </b-col>
              </b-row>
            </b-container>


            <b-card class="userAbout">
              <b-card-text class="aboutMeTitle">Обо мне</b-card-text>
              <b-card-text class="aboutMeText">
                Город: {{getUserFeed.data[currentUser].city_title}}, Пол: {{getUserFeed.data[currentUser].sex ? "Женский" : "Мужской" }}
              </b-card-text>
            </b-card>

          </b-card>
      </div>
    </div>
    <div v-if="(currentUser === -1 || getUserFeed.data.length === 0) && getUserFeed.loaded" class="noFeed">
      <b-container>
        <b-row class="justify-content-md-center">
          <img alt="no_feed" src="../assets/cat.webp" class="noFeedPhoto">
        </b-row>
        <b-row class="justify-content-md-center">
          <h3>Больше нет анкет ;(</h3>
        </b-row>
      </b-container>
    </div>

  </div>
</template>

<script>
import {mapActions, mapGetters} from "vuex";

export default {
  name: "FeedView",
  data() {
    return {
      currentUser: 0,
      items: ["Москва", "Рыбы", "INFJ-A", "Игры", "Готовка"]
    }
  },
  methods: {
    ...mapActions(["fetchFeed", "setLike", "fetchCurrentUser"]),
    async dislikeButton() {
      if (this.currentUser + 1 !== this.getUserFeed.data.length) {
        this.currentUser += 1;
        await this.fetchCurrentUser(this.getUserFeed.data[this.currentUser].user_id)
      } else {
        this.currentUser = -1;
      }
    },
    async likeButton() {
      let user = new FormData();
      user.append("to_user_id", this.getUserFeed.data[this.currentUser].user_id);
      await this.setLike(user);

      if (this.getUserLike.match) {
        console.log(this.getUserLike.match);
      } else {
        console.log("No match")
      }

      if (this.currentUser + 1 !== this.getUserFeed.data.length) {
        this.currentUser += 1;
        await this.fetchCurrentUser(this.getUserFeed.data[this.currentUser].user_id);
      } else {
        this.currentUser = -1;
      }
    }
  },
  computed: {
    ...mapGetters(["getUserFeed", "getUserLike", "getCurrentUser"])
  },
  async mounted() {
    await this.fetchFeed();
    if (this.getUserFeed.loaded) {
      await this.fetchCurrentUser(this.getUserFeed.data[0].user_id);
    }
  },
  // created() {
  //   this.fetchFeed();
  // }
}
</script>
<style scoped>
  .containerAlignmentForm {
    height: 100%;
    align-content: center;
    padding-top: 2%;
  }

  .userFormCard {
    width: 730px;
  }

  .userPhotoCard {
    width: 420px;
    height: 420px;
    overflow: hidden;
  }

  .userPhoto {
    width: 100%;
    height: 100%;
    object-fit: cover;
    object-position: center;
  }

  .userFormNameAge {
    color: #6724FF;
    font-size: 33px;
    text-align: center;
  }

  .interest {
    width: 102px;
    height: 30px;
    margin-bottom: 10px;
  }

  .interest > .card-body {
    padding: 0 !important;
  }

  .interestTitle {
    color: #6724FF;
    font-size: 14px;
    text-align: center;
  }

  .userAbout {
    margin-top: 20px;
  }

  .aboutMeTitle {
    color: #6724FF;
    font-size: 16px;
    font-weight: 700;
  }

  .aboutMeText {
    color: #6724FF;
    font-size: 16px;
  }

  .noFeed {
    padding-top: 10%;

  }

  .noFeedPhoto {
    width: 500px;
    height: auto;
    display: block;
  }

</style>