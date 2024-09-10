<template>
    <div>
        <Title :title="complexData" />
        <v-container>
            <v-row>
                <v-col col="12">
                    <v-card>
                        <v-card-title>
                            跟踪记录器（Tracker）
                        </v-card-title>
                        <v-card-text>
                            根据9月7日的 7af6b027ac8139fc ，四原则中的记录性质，需要记录日程，任务，账单三项。这个项目可以方便记录日程和任务。
                        </v-card-text>
                        <v-card-text>
                            预计部署在tracker.teyvatedu.cn中，仅供个人使用。
                        </v-card-text>
                    </v-card>
                </v-col>
            </v-row>
        </v-container>
    </div>
</template>


<script>    
import Title from '../components/TitlePage.vue'
export default {
    components: {
        Title
    },
    name: 'HomeView',
    data() {
        return {
            complexData: {
                title: 'Tracker Site',
                subtitle: '',
                description: ''
            }

        }
    }
}

</script>