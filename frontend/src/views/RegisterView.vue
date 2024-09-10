<template>
     <v-container fluid>
        
      <v-row justify="center">
        <v-col cols="12" sm="8" md="4">
          <v-card class="elevation-12">
            <v-toolbar color="primary" dark flat>
              <v-toolbar-title>{{formType == 'register' ? '用户注册' : '忘记密码'}}</v-toolbar-title>
            </v-toolbar>
            <v-card-text>
              <v-form ref="form" v-model="valid" lazy-validation>
                <v-text-field
                  v-model="formData.email"
                  label="注册邮箱"
                  :rules="[rules.required]"
                  required
                  prepend-icon="mdi-email"
                ></v-text-field>
                <v-text-field
                  v-if="formType == 'register'"
                  v-model="formData.username"
                  label="用户名"
                  :rules="[rules.required]"
                  required
                  prepend-icon="mdi-account"
                ></v-text-field>
                <v-text-field
                  v-if="formType == 'register'"
                  v-model="formData.password"
                  label="密码"
                  :rules="[rules.required]"
                  required
                  prepend-icon="mdi-lock"
                  type="password"
                ></v-text-field>
              </v-form>
            </v-card-text>
            <v-card-actions>
              <v-btn color="primary" :disabled="!valid" @click="submit" block>{{formType == 'register' ? '注册' : '验证邮箱'}}</v-btn>
            </v-card-actions>
          </v-card>
        </v-col>
      </v-row>
     </v-container>
</template>


<script>
export default {
  name: "RegisterView",
  data() {
    return {
      formType: "",
      formData:{
        email: "",
        username: "",
        password: "",
      },
      valid: false,
      userString: "",
      rules: {
        required: v =>!!v || "必填项不能为空",
      }
    }   
  },
  methods: {
    submit() {
      this.$refs.form.validate()
      if (this.valid) {
        // do something
      }
    },
  },
    created(){
        let query = this.$route.query;
        if(query.type == "forget"){
            this.formType = "forget";
        }else{
            this.formType = "register";
        }
    }
}
</script>