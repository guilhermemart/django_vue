<template>
    <div class="box">
        <span class="content is-small">Label: {{ label }}</span>
        <span class="content is-small">Data: {{ data }}</span>
    </div>
</template>
<script>
export default {
    props: {
        label: String,
        data: String
    }
}
</script>