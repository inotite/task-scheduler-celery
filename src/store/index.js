import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)
export default new Vuex.Store({
  state: {
    authenticated: false,
    isCreatingNewTask: false,
    tasks: {}
  },
  getters: {
    tasks: state => state.tasks
  },
  mutations: {
    setAuthenticated (state) {
      state.authenticated = !state.authenticated
    },
    setIsCreatingNewTask (state) {
      state.setIsCreatingNewTask = !state.isCreatingNewTask
    },
    setTasks (state, payload) {
      state.tasks = payload
    },
    clearCreatingNewTask (state) {
      state.isCreatingNewTask = false
    }
  },
  actions: {
    setTasks ({ commit }, payload) {
      commit('setTasks', payload)
    },
    clearCreatingNewTask ({ commit }) {
      commit('clearCreatingNewTask')
    }
  }
})
