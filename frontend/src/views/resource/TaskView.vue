<template>
    <div>
        <v-row>
            <v-col justify="center">
                <h1 class="text-center">Task Create</h1>
            </v-col>
        </v-row>
        
        <v-container>
            <!--create task form-->
            <v-row>
                <v-col cols="12">
                    <v-card>
                        <v-card-title>Create Task</v-card-title>
                        <v-card-text>
                            <v-form>    
                                <v-text-field label="Title" v-model="formData.title"></v-text-field>
                                <v-textarea label="Description" v-model="formData.description"></v-textarea>
                                <v-radio-group v-model="radioGroup">
                                    <!-- 0 : not planned, 1: pending, 2: Noticed, 3: Completed 4: Archived -->
                                    <v-radio
                                        v-for="n in 3"
                                        :key="n"
                                        :label="['Not Planned', 'Pending', 'Noticed', 'Completed', 'Archived'][n]"
                                        :value="n"
                                    ></v-radio>
                                    </v-radio-group>
                                <!--Priority Depricated-->
                                <v-row>
                                    <v-col cols="3">
                                        <v-btn block @click="addDays(1)" color="success">+1天</v-btn>
                                    </v-col>
                                    <v-col cols="3">
                                        <v-btn block @click="addDays(-1)" color="red">-1天</v-btn>
                                    </v-col>
                                    <v-col cols="3">
                                        <v-btn block @click="addHours(1)" color="success">+1小时</v-btn>
                                    </v-col>
                                    <v-col cols="3">
                                        <v-btn block @click="addHours(-1)" color="red">-1小时</v-btn>
                                    </v-col>
                                    
                                </v-row>
                                <v-row justify="center">
                                    <v-col cols="6">
                                        <v-row justify="center">
                                            <v-date-picker v-model="datePickerValue"></v-date-picker>
                                        </v-row>
                                        
                                    </v-col>
                                    <v-col cols="6">
                                        <v-row justify="center">
                                        <v-time-picker
                                        use-seconds
                                        full-width
                                        v-model="timePickerValue"
                                        ampm-in-title
                                        format="ampm"
                                        
                                        scrollable
                                        ></v-time-picker>
                                    </v-row>
                                    </v-col>
                                </v-row>
                                
                                <!--BTN: UPDATE or CREATE-->
                                <v-btn @click="createTask" class="my-2" color="primary" block>{{ this.$route.query.id? 'Update' : 'Create' }}</v-btn>
                            </v-form>
                        </v-card-text>
                    </v-card>
                </v-col>
            </v-row>
            <!--task list-->
            <v-row>
                <v-col cols="12">
                    <v-card>
                        <v-card-title>
                            Tasks
                        <v-spacer></v-spacer>
                        <v-text-field
                            v-model="search"
                            append-icon="mdi-magnify"
                            label="Search"
                            single-line
                            hide-details
                        ></v-text-field>
                        </v-card-title>
                        <v-simple-table>
                            <template v-slot:default>
                            <thead>
                                <tr>
                                <th class="text-left">ID</th>
                                <th class="text-left">名称</th>
                                <th class="text-left">Description</th>
                                <!--
                                <th class="text-left">Priority</th>
                                <th class="text-left">Assignee</th>
                                -->
                                
                                <th class="text-left">Start Time</th>
                                <th class="text-left">Remaining Time</th>
                                <th class="text-left">Status</th>
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
                                <!--
                                
                                <td>{{ item.task_priority }}</td>
                                <td>{{ item.task_assignee }}</td>
                                -->
                                <td>{{ parseDate(item.task_start_time) }}</td>
                                <td>{{ getRemainingTime(item.task_start_time) }}</td>
                                <td>{{ item.task_status }}</td>

                                </tr>
                            </tbody>
                            </template>
                        </v-simple-table>
                        </v-card>
                </v-col>
            </v-row>
        </v-container>
    </div>
</template>
<script>
import {getUserId} from "@/utils";
import http from '@/http'
export default {
    name: 'TaskView',
    data() {
        return {
            search:'',
            formData: {
                title: '',
                description: ''
            },
            poririty: 3,
            radioGroup: 1,
            tasks: [],
            datePicker: null,
            timePicker: null,
            mode:'',
        }
    },
    computed: {
        datePickerValue:{
            get(){
                return this.datePicker
            },
            set(value){
                //convert date string to date object
                let dateArr = value.split('-');
                let selectedDate = new Date(dateArr[0], dateArr[1]-1, dateArr[2]);
                // if earlier than today, set to today
                if(selectedDate < new Date()){
                    selectedDate = new Date();
                }
                this.datePicker = selectedDate.toLocaleDateString().split('/').join('-');
            }
        },
        timePickerValue:{
            get(){
                return this.timePicker;
            },
            set(value){
                this.timePicker = value;
            }
        }
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
            console.log(item)
        },
        addDays(d){
            let dateString = this.datePickerValue.split('-');
            let year = dateString[0];
            let month = dateString[1];
            let day = dateString[2];
            let date = new Date(year, month - 1, day);
            date.setDate(date.getDate() + d);
            this.datePickerValue = date.toLocaleDateString().split('/').join('-');
        },
        addHours(h){
            let timeString = this.timePicker;
            let [hour, minute, second] = timeString.split(':').map(Number);
            let newHour = hour + h;
            let newMinute = minute;
            let newSecond = second;
            if(newHour < 0){
                newHour = 23;
            }
            if(newHour > 23){
                newHour = 0;
            }
            if(newMinute < 0){
                newMinute = 59;
            }
            if(newMinute > 59){
                newMinute = 0;
            }
            if(newSecond < 0){
                newSecond = 59;
            }
            if(newSecond > 59){
                newSecond = 0;
            }
            this.timePicker = `${newHour}:${newMinute}:${newSecond}`;
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
        createTask(){
            let userId = getUserId();
            // 2024-09-09T13:28:35.592Z is ISO format for date and time, datepicker and timepicker return string in this format
            let date = this.formatDateToISO(this.datePicker, this.timePicker);
            let taskStartTime = date;
            if(this.mode === 'put'){
                http.put("/task/update/task?id=" + this.$route.query.id,{
                    task_start_time: taskStartTime,
                    task_status: this.radioGroup,
                    task_name: this.formData.title,
                    task_description: this.formData.description,
                    task_priority: 1,
                    task_assignee: userId,
                }).then(response => {
                    console.log(response.data)
                }).catch(error => {
                    console.log(error)
                })
                return;
            }
            http.post("/task/new/task",{
                task_start_time: taskStartTime,
                task_status: this.radioGroup,
                task_name: this.formData.title,
                task_description: this.formData.description,
                task_priority: 1,
                task_assignee: userId,
            }).then(response => {
                console.log(response.data)
            }).catch(error => {
                console.log(error)
            })
        },
        fetchTasks(){
            http.get("/task/all").then(response => {
                this.tasks = response.data;
                console.log(response.data)
            })
            let currentDateStr = new Date().toLocaleDateString().split('/').join('-');
            let currentTimeStr = new Date().toLocaleTimeString();
            this.datePicker = currentDateStr;
            this.timePicker = currentTimeStr;
        },
        fetchByID(id){
            http.get("/task/taskByID?id="+id).then(response => {
                console.log(response.data)
                this.formData.title = response.data.task_name;
                this.formData.description = response.data.task_description;
                this.radioGroup = response.data.task_status;
                this.datePicker = response.data.task_start_time.split('T')[0];
                let timeStr = response.data.task_start_time.split('T')[1].split('+')[0];
                this.timePicker = timeStr;
                console.log(this.datePicker)
                console.log(this.timePicker)
            })
        }
    },
    mounted() {
        this.fetchTasks()
    },
    created() {
        //let query = this.$route.params;
        console.log(this.$route.query)
        if(this.$route.query.id){
            // modify mode
            this.mode = 'put';
            this.fetchByID(this.$route.query.id);
        }
    }
}

</script>