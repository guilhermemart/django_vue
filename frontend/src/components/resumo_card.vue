<template>
  <div>
    <div class="box has-background-white mx-1">
      <div class="mb-5">
        <span class="is-size-3 has-text-weight-bold">{{monthlyData.month}}</span>
      </div>
      <div class="has-text-underlined mb-2">
        <span class="is-size-5 has-text-weight-bold">Total de alertas: {{monthlyData.total}}</span>
      </div>
      <div class="has-text-underlined mb-2">
        <span class="is-size-6 has-text-weight-bold has-text-primary">EPI: 0</span>
      </div>
      <div class="has-text-underlined mb-2">
        <span class="is-size-6 has-text-weight-bold has-text-primary">Red Zones: 0</span>
      </div>

      <div class="has-text-underlined mb-2">
        <span class="is-size-6 has-text-weight-bold has-text-success">Aprovado: {{monthlyData.approved}}</span>
      </div>

      <div class="has-text-underlined mb-2">
        <span class="is-size-6 has-text-weight-bold has-text-danger">Reprovado: {{monthlyData.disapproved}}</span>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    monthlyData: Object
  },
  data() {
    return {
    }
  },
}
</script>

<style scoped>

</style>