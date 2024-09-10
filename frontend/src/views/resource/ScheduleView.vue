<template>
    <div>
        <h1 class="text-center">Schedule</h1>
        <!--
        input form: title, desc, place, date
        -->
        <v-container>
        <v-row>
            <v-col cols="12"> 
                <v-card>
                    <v-card-title>
                        <h2 class="headline mb-0">Create a new event</h2>
                    </v-card-title>
                    <v-card-text>
                        <v-form>
                              <v-text-field label="Title" v-model="title"></v-text-field>
                              <v-text-field label="Description" v-model="desc"></v-text-field>
                              <v-text-field label="Place" v-model="place"></v-text-field>
                              <v-row justify="center">
                                  <v-date-picker v-model="date"></v-date-picker>
                              </v-row>
                              <v-btn color="primary" @click="createEvent">Create</v-btn>
                            </v-form>
                    </v-card-text>
                </v-card>
            </v-col>
        </v-row>
        <v-row>
          <v-col cols="12">
            <v-card>
              <v-card-title>
                All Schedule: not available
              </v-card-title>
              <v-card-text>
                <v-simple-table>
                  <template #no-data>
                            Schedule Data is not available.
                  </template>
                </v-simple-table>
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>
      </v-container>
    </div>
</template>

<script>
import http from '@/http'
import {getUserId} from '@/utils'
export default {

  name: 'ScheduleView',
  data() {
    return {
      title: '',
      desc: '',
      place: '',
      date: ''
    }
},
  methods: {
    createEvent() {
      let user_id = getUserId()
      http.post("/schedule/new",
        {
          schedule_date:this.date,
          schedule_place:this.place,
          schedule_title:this.title,
          schedule_description:this.desc,
          user_id:user_id
        }
      ).then(resp => {
        console.log(resp.data);
      })
      console.log('create event');
    },
    initDate(){
      let today = new Date().toISOString().split('T')[0];
      this.date = today
      console.log(this.date)
    }
  },
  mounted() {
    this.initDate();
  }
}
</script>