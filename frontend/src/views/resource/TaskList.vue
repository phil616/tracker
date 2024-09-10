<template>
    <v-container>
            <v-row>
                <v-col cols="12">
                    <h1 class="headline mb-0 text-center">Task List</h1>
                </v-col>
            </v-row>
            <v-card>
                <v-card-title>
                    
                </v-card-title>
                <v-simple-table>
                            <template v-slot:default>
                            <thead>
                                <tr>
                                <th class="text-left">ID</th>
                                <th class="text-left">名称</th>
                                <th class="text-left">Description</th>
                                
                                <th class="text-center">Start Time</th>
                                <th class="text-center">Remaining Time</th>
                                <th class="text-center">Status</th>
                                <th class="text-center">Action</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr
                                v-for="item in tasks"
                                :key="item.name"
                                >
                                <td>{{ item.task_id }}</td>
                                <td>{{ item.task_name }}</td>
                                <td>{{ item.task_description }}</td>
                                <td>{{ parseDate(item.task_start_time) }}</td>
                                <td>{{ getRemainingTime(item.task_start_time) }}</td>
                                <td>{{ item.task_status }}</td>
                                <td>
                                    <v-btn color="primary" class="mr-2" @click="editTask(item)">Edit</v-btn>
                                    <v-btn color="error" @click="deleteTask(item)">Delete</v-btn>
                                </td>
                                </tr>
                            </tbody>
                            </template>
                        </v-simple-table>
            </v-card>
    </v-container>
</template>
<script>
import http from '@/http'
export default {
    name: "TaskList",
    data() {
        return {
            tasks: []
        };
    },
    created() {
        
    },
    methods: {
        getRemainingTime(dateString){
            let date = new Date(dateString);
            let now = new Date();
            let diff = (now - date) / 1000;
            let remainingSeconds = Math.floor(diff % 60);
            let remainingMinutes = Math.floor((diff / 60) % 60);
            let remainingHours = Math.floor((diff / 3600) % 24);
            let remainingDays = Math.floor(diff / 86400);
            if(remainingDays > 0){
                return `${remainingDays} days`;
            }
            if(remainingHours > 0){
                return `${remainingHours} hours ${remainingMinutes} minutes`;
            }
            if(remainingMinutes > 0){
                return `${remainingMinutes} minutes ${remainingSeconds} seconds`;
            }
            return `${remainingSeconds} seconds`;
        },
        parseDate(dateString){
            // dateString format is ISOString
            let date = new Date(dateString);
            return date.toLocaleDateString() + " " + date.toLocaleTimeString();
        },
        editTask(item){
            this.$router.push({name: "Task", query: {id: item.task_id}})
        },
        deleteTask(item){
            http.get("/task/cancel?id="+item.task_id).then(response => {
                console.log(response.data)
                alert("Task Cancelled successfully")
            })
            this.fetchTasks()
            console.log(item)
        },
        formatDateToISO(dateString,timeString) {
                // 将日期字符串拆分为年、月、日
                let [year, month, day] = dateString.split('-').map(Number);
                // 将时间字符串拆分为时、分、秒
                let [hour, minute, second] = timeString.split(':').map(Number);
                // 将时、分、秒转换为毫秒
                let millisecond = hour * 3600000 + minute * 60000 + second * 1000;
                // 创建一个日期对象
                let date = new Date(year, month - 1, day, 0, 0, 0, 0);
                // 加上毫秒
                date.setMilliseconds(millisecond);
                // 返回 ISO 格式的日期字符串
                return date.toISOString();
        },
        debug() {
            this.$router.push("/task?id=2");
            console.log("debug");
        },
        getTasks() {
            
        },
        
        fetchTasks(){
            http.get("/task/all").then(response => {
                    this.tasks = response.data;
                    console.log(response.data)
            })
        }
    },
    mounted() {
        this.fetchTasks()
    },
};
</script>