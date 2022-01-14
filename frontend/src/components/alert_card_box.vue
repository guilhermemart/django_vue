<template>
    <div class="has-rounded-border has-text-grey-dark has-text-centered">
        <span class="has-text-weight-bold is-size-8 is-block">{{ Label }}</span>
        <span class="is-size-8 is-block">{{ Data }}</span>
    </div>
</template>
<style lang="scss" scoped>
.has-rounded-border {
    padding: .01vh .10vw .01vh;
    border: .5px solid grey;
    border-radius: 8px;
    margin-top: 1vh;
}

.is-size-8 {
    font-size: 1.60vh;
}
</style>
<script>
export default {
    props: {
        Label: String,
        Data: String
    }
}
</script>