import { createStore } from 'vuex'

export default createStore({
  state: {
    audio: {
        is_on: true,
        is_instantaneo: true,
        is_recorrente: true,
        has_delay: true
    },
    filter:{
        valid: true,
        invalid: true,
        non_classified: true,
        date_start: 0,
        date_end:new Date().getTime()
    },
    isAuthenticated: false,
    token: '',
    isLoading: false
  },
  mutations: {
    initializeStore(state) {
      if (localStorage.getItem('audio')) {
        state.audio = JSON.parse(localStorage.getItem('audio'))
      } else {
        localStorage.setItem('audio', JSON.stringify(state.audio))
      }
      if (localStorage.getItem('filter')) {
        state.audio = JSON.parse(localStorage.getItem('filter'))
      } else {
        localStorage.setItem('filter', JSON.stringify(state.audio))
      }
      if (localStorage.getItem('token')) {
          state.token = localStorage.getItem('token')
          state.isAuthenticated = true
      } else {
          state.token = ''
          state.isAuthenticated = false
      }
    },
    save_audio(state, audio_new) {
      state.audio.is_on = audio_new.is_on
      state.audio.is_instantaneo = audio_new.is_instantaneo
      state.audio.is_recorrente = audio_new.is_recorrente
      state.audio.has_delay = audio_new.has_delay
      localStorage.setItem('audio', JSON.stringify(state.audio))
    },
    setIsLoading(state, status) {
      state.isLoading = status
    },
    setToken(state, token) {
        state.token = token
        state.isAuthenticated = true
    },
    removeToken(state) {
        state.token = ''
        state.isAuthenticated = false
    },
  },
  actions: {
  },
  modules: {
  }
})