<template>
  <div>
    <div class="box has-background-white">
      <div class="mb-5">
        <span class="is-size-3 has-text-weight-bold">{{monthlyData.month}}</span>
      </div>
      <div class="has-text-underlined mb-2">
        <span class="is-size-4 has-text-weight-bold">Total of alerts: {{monthlyData.total}}</span>
      </div>
      <div class="has-text-underlined mb-2">
        <span class="is-size-5 has-text-weight-bold has-text-primary">PPE: {{monthlyData.nonconformity}}</span>
      </div>
      <div class="has-text-underlined mb-2">
        <span class="is-size-5 has-text-weight-bold has-text-primary">Red Zones: {{monthlyData.redzone}}</span>
      </div>

      <div class="has-text-underlined mb-2">
        <span class="is-size-5 has-text-weight-bold has-text-success">Approved: {{monthlyData.approved}}</span>
      </div>

      <div class="has-text-underlined mb-2">
        <span class="is-size-5 has-text-weight-bold has-text-danger">Disapproved: {{monthlyData.disapproved}}</span>
      </div>

      <div class="has-text-underlined mb-2">
        <span class="is-size-5 has-text-weight-bold has-text-warning">Unclassified: {{monthlyData.unclassified}}</span>
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