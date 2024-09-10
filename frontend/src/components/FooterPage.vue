<template>
  <footer class="footer">
    <div class="footer-bottom">
      <p>@phil616 {{ new Date().getFullYear() }} , All rights reserved.
        <a v-for="(item, index) in footerLinks" :key="index" :href="item.link" class="a"><span class="footer-ref">| {{ item.name }} </span></a>
      </p>
    </div>
  </footer>
</template> 

<script>
export default {
  data(){
    return {
        footerLinks:[
            {
                name: "关于",
                link: "/about"
            },
            {
                name: "Github",
                link: "https://www.github.com/phil616/tracker"
            }
        ]
    };
  }
}
</script>

<style scoped>
.footer {
  background-color: #282c34;
  color: white;
  padding: 20px;

}
.a {
    text-decoration: none;
}
.footer-ref{
  color: white;
}
p {
  margin: 0;
    font-size: 14px;
}
.social-icons {
  margin-top: 10px;
}

@media (min-width: 768px) {
  .footer-ref {
    flex-direction: row;
    justify-content: space-around;
  }

  .footer-section {
    border: none;
    padding: 0;
  }

  .footer-title {
    margin-bottom: 10px;
  }
}
</style>
