<template>
    <div class="title-page text-center">
        <h1 class="center-text"> {{  title.title }} </h1>
    </div>
</template>

<script>
/*
    props data structure declaration:
    props name: title
    props type: String
    props required: true

*/
export default {
    name: 'TitlePage',
    props: {
        title: {
            required: true
        }
    },
    data() {
        return {
        }
    },
    methods: {
    },
    created() {
         // console.log('TitlePage created', this.title);
    }
}
</script>

