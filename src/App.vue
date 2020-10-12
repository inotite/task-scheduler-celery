<template>

  <div id="app">
    <nav id="navbar" style="background-color:#ffd900" ref="navHeight">
      <div class="navbar-brand">
            <a href="/">
             <img src="./assets/sagenew.png">
            </a>
            </div>
            <ul>
            <div class="navbar-content">
                <li class="dropdown">
                     <a>
                    <machinedropdown @keySelected="setSelectedKey" :options="options"></machinedropdown>
                     </a>
                 </li>
              </div>
           <!-- login section holds login/logout-->
              <div class="login">
                 <li v-if="!$store.state.authenticated">
                   <a>
                     <!-- only display login button if not already authenticated, onclick show login modal-->
                     <button class="btn btn-secondary" v-if="!$store.state.authenticated" @click="showLoginModal = true">
                       Login
                     </button>
                    </a>
                 </li>
                 <li>
                   <a><button class="btn btn-secondary" v-if="$store.state.authenticated" @click="$store.commit('setAuthenticated')">Logout</button></a>
                 </li>
              </div>
          </ul>
    </nav>
   <loginmodal v-if="showLoginModal"></loginmodal>
   <!--<tasks v-if="!selectedKey==''" :selectedKey="selectedKey" :json="options" :navHeight="navHeight" @taskStatusUpdated="updateTaskStatus" @payloadSubmitted="postDataToApi"></tasks>
   -->
   <v-alert v-if="submitSuccess" type="success" border="left" dismissable="true"></v-alert>
   <router-view></router-view>
 </div>

</template>

<script>

import axios from 'axios'
import machinedropdown from './components/MachineDropdown.vue'
import tasks from './components/Tasks.vue'
import loginmodal from './components/LoginModal'

export default {
  name: 'App',
  components: {
    machinedropdown,
    tasks,
    loginmodal
  },
  data () {
    return {
      isLoggingIn: false,
      selectedKey: '',
      options: {},
      submitSuccess: false,
      showLoginModal: false,
      // mockAccount holds login credentials until db is set up
      mockAccount: {
        username: 'alexander',
        password: 'password'
      }
    }
  },
  created () {
    this.fetchTasks()
  },
  methods: {
    fetchTasks () {
      axios.get(`${process.env.BASE_URL}/tasks`)
        .then(response => response.data)
        .then(response => {
          const tasks = this._.groupBy(response, (el) => el.machine)
          for (const key in tasks) {
            const value = {}
            tasks[key].forEach(task => {
              value[`key-${task.id}`] = task
            })
            console.log(value)
            this.$set(this.options, key, value)
          }
          this.$store.commit('setTasks', this.options)
        })
        .catch(err => {
          console.log(err)
        })
    },
    setIsLoggingIn () {
      this.isLoggingIn = !this.isLoggingIn
    },
    updateJson (updatedJson) {
      this.options = updatedJson
    },
    reroute () {
      this.$router.push('/tasks')
    },
    setSelectedKey (selectedKey) {
      this.selectedKey = selectedKey
      this.changeRoute(selectedKey)
    },
    updateTaskStatus () {
      console.log('this is the options: ' + JSON.stringify(Object.values(this.options[this.selectedKey])))
      console.log('this is the options after update: ' + JSON.stringify(Object.values(this.options[this.selectedKey])[0].completed))
    },
    changeRoute (selectedKey) {
      console.log(this.options)
      this.$router.push({name: 'Tasks', params: { machineId: selectedKey }})
        .catch(err => console.log(err))
    }
  },
  computed: {
    navHeight: function () {
      return this.$refs.navHeight.clientHeight
    }
  }
}

</script>

<style>

/* navbar to  house navigation bar */
#navbar{
  /* make navbar sticky */
  position: -webkit-sticky;
  position: sticky;
  top: 0;
  margin-bottom:0;
  padding-left:0;
  list-style: none;
  background-color: #ffd503;
  border-color: #e7e7e7;
}
#navbar>li{
   list-style-type: none;
   margin: 0;
   padding: 0;
   position:relative;
   display:block;
   width:100%;
}
li a{
   display: inline-block;
   padding: 4px 16px;
}
#navbar ul{
   list-style-type: none;
   overflow: hidden;
   background-color: #ffd503;
}
li a:hover {
    background-color: #FFFF00;
    color: #000000;
}
#navbar>li>a{
   position:relative;
   display:block;
}
.navbar-content{
  width: 30%;
  margin-right: auto;

}
.login{
  float: right;
  height: 100%;
}
.login li {
  vertical-align: middle;
}
.navbar-brand{
   padding-top:35px;
   height: 50px;
   width:30%;
   vertical-align: middle;
   margin: 0 auto;
   float: left;
}
.navbar-brand img{
   height: auto;
   width: 150px;
   border-style: none;
   vertical-align: middle;
}
.navbar-content{
   height: 100%;
   margin: 0;
}
body {
        background-color: #F0F0F0;
    }
h1 {
        padding: 0;
        margin-top: 0;
    }
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

</style>
