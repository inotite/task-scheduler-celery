import Vue from 'vue'
import VueLodash from 'vue-lodash'
import lodash from 'lodash'
import App from './App.vue'
import { BootstrapVue, IconsPlugin } from 'bootstrap-vue'
import 'bootstrap/dist/css/bootstrap.min.css'
import store from './store'
import router from './router'
import VueSimpleAlert from 'vue-simple-alert'

Vue.use(VueSimpleAlert)
Vue.use(BootstrapVue)
Vue.use(IconsPlugin)
Vue.use(VueLodash, { lodash })

Vue.config.productionTip = false

new Vue({
  store,
  router,
  render: h => h(App)
}).$mount('#app')
