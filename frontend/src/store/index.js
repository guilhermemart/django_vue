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
        //date_end:new Date().getTime(),
        date_end:2500916953418
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
        state.filter = JSON.parse(localStorage.getItem('filter'))
      } else {
        localStorage.setItem('filter', JSON.stringify(state.filter))
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
    save_filter(state, filter_new) {
      state.filter.valid = filter_new.valid
      state.filter.invalid = filter_new.invalid
      state.filter.non_classified = filter_new.non_classified
      state.filter.date_start = filter_new.date_start
      state.filter.date_end = filter_new.date_end
      localStorage.setItem('filter', JSON.stringify(state.filter))
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