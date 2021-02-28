<template>
  <div>
    <v-row>
      <v-col md="4" offset-md="4" sm="12" offset-sm="0">
        <v-card class="p-4">
          <h1>Register</h1>
          <v-form @submit.prevent="register">
            <v-text-field
              v-model="email"
              label="E-mail"
              :rules="emailRules"
              required
            ></v-text-field>
            <v-text-field
              v-model="password"
              label="Password"
              type="password"
              :rules="passwordRules"
              required
            ></v-text-field>
            <v-text-field
              v-model="repeatPassword"
              label="Repeat Password"
              type="password"
              :rules="passwordRules"
              required
            ></v-text-field>
            <v-alert
              class="mt-1"
              type="error"
              dense
              outlined
              v-if="errorMessage"
              >
              {{ errorMessage }}
            </v-alert>
            <v-btn color="#173450" dark large type="submit">Register</v-btn>
          </v-form>
        </v-card>
      </v-col>
    </v-row>
  </div>
</template>
<script>
import firebase from 'firebase/app'
import 'firebase/auth'

export default {
  name: 'Register',
  asyncData() {
    return {
      authenticatedUser: null,
      email: '',
      password: '',
      repeatPassword: '',
      errorMessage: '',
    }
  },
  methods: {
    async register() {
      if (this.password !== this.repeatPassword) {
        this.errorMessage = 'The two provided passwords do not match!';
        return;
      }

      await firebase.auth().createUserWithEmailAndPassword(this.email, this.password)
      .then((user) => {
        this.$router.push('/submit-event');
      })
      .catch((error) => {
        this.errorMessage = error.message;
      });
    },
  },
  created() {
    firebase.auth().onAuthStateChanged(user => {
      this.authenticatedUser = user;
    });
  },
  computed: {
    passwordRules() {
      const rules = [];

      const passwordRequired = v => !!v || 'Password is required';
      rules.push(passwordRequired);

      const repeatPasswordRequired = v => !!v || 'Repeat Password is required';
      rules.push(repeatPasswordRequired);

      if (this.repeatPassword) {
        const rule = v => (!!v && v) === this.password || 'Passwords do not match';
        rules.push(rule);
      }

      return rules;
    }
  },
  data() {
    return {
      emailRules: [
        v => !!v || 'E-mail is required',
        v => /.+@.+\..+/.test(v) || 'E-mail must be valid',
      ],
    };
  }
}
</script>