<template>
  <v-container>
    <div class="d-flex">
    <h1 class="ma-0">Лабубу стор</h1> 
    <v-text-field variant="solo-filled" 
      prepend-inner-icon="mdi-magnify" 
      rounded 
      placeholder="Найти лабубу"
      class="ml-10"
      v-model="searchString"
    ></v-text-field>
    </div>
    <v-data-table :headers="headers" :items="labubu">
      <template v-slot:item.actions="{item}" >
        <v-dialog max-width="500" v-model="isEditNewEntity2">
          <template v-slot:activator="{ props: activatorProps }">
            <v-btn v-bind="activatorProps"
            color="grey"
            icon="mdi-pencil"
            @click="get(item.name)"
            class="mx-3"
            >
          </v-btn>
            <v-btn 
            color="red"
            icon="mdi-delete"
            variant="elevated"
            @click="SmertLabubi(item.id)">
          </v-btn>

          </template>
          <template v-slot:default="{isActive}">
            <v-card title = "Изменить Лабубе">
              <v-spacer></v-spacer>
              <v-text-field variant="solo-filled" v-model="dataTadaData.name"></v-text-field>
              <v-text-field variant="solo-filled" v-model="dataTadaData.description"></v-text-field>
              <v-card-actions>
                <v-btn
              text="Я не хожу на лево"
              @click="isActive.value = false"
              ></v-btn>
              <v-spacer></v-spacer>
              <v-btn 
              text="подтвердить измену"
              @click=put>
              </v-btn>
              </v-card-actions>
            </v-card>

          </template>
        </v-dialog>
      </template>
    </v-data-table>
  </v-container>
  <v-container>
    <v-dialog max-width="500" v-model="isEditNewEntity">
      <template v-slot:activator="{ props: activatorProps }">
        <v-btn v-bind="activatorProps"
          color="grey"
          text="Добавить Лабубу Мечты"
          variant="flat"
          >
        </v-btn>
      </template>

      <template v-slot:default="{ isActive }">
        <v-card title = "Лабубааааа">
          <v-spacer></v-spacer>
          <v-text-field placeholder="Ввведите имя лабубы вашей мечты" variant="solo-filled" v-model="dataTadaData.name"></v-text-field>
          <v-text-field placeholder="введите описание лабубы вашей мечты" variant="solo-filled" v-model="dataTadaData.description"></v-text-field>
          <v-card-actions>
            <v-btn
              text="Я передумал"
              @click="isActive.value = false"
            ></v-btn>
            <v-spacer></v-spacer>
            <v-btn
              text="Отправить"
              @click=createlabubu
            ></v-btn>
          </v-card-actions>
        </v-card>
      </template>

    </v-dialog>
  </v-container>

  
</template>

<script setup lang="ts">
import axios from 'axios';
import { onMounted, ref, watch } from 'vue';

const isEditNewEntity =ref(false)
const isEditNewEntity2 =ref(false)

const searchString = ref('')

const labubu = ref<{name: string; description: string}[]>([])

const dataTadaData = ref({
  name: '',
  description: '',
  id: ""
})
function clearAll(){
  dataTadaData.value.name = "",
  dataTadaData.value.description =""
}


function createlabubu() {
  if (dataTadaData.value.name == "") {
    console.log("у тебя не заполнено поле имя!!!")
    return 
  } 
  if (dataTadaData.value.description == "") {
    console.log("у тебя не заполнено поле описание!!!")
    return
  } 
 axios.post("/labubu/create", {
  name: dataTadaData.value.name,
  description: dataTadaData.value.description
 })
  .then((response)=>{
    console.log("Успех", response.data)
  })
  .then (GetAllData)
  .then (()=>{
    isEditNewEntity.value = false
  }) 
  .then (clearAll)
  .catch((error)=>{
    if (error.response.status === 404) {
      alert('Лабубу вмер')
    }
  })
}

function GetAllData() {
axios.get('/labubu/get_list',{
  params: {search_str: searchString.value}
})
  .then((response)=>{
    console.log(response.data);
    labubu.value = response.data
  })
  .catch((error)=>{
    if (error.response.status === 404) {
      alert('Лабубу вмер')
    }
  })
}

const headers =ref([
  {title: "Название", key: "name"},
  {title: "Описание", key: "description"},
  {title: "Actions", key: "actions", width: "200px"

  }
])



function get(name: string){
  axios.get(`/labubu/get/${name}`)
  .then((response)=>{
    dataTadaData.value = response.data
    console.log(response.data)
  })
  
}

function put(){
  axios.put(`/labubu/update/${dataTadaData.value.id}`,{
    name: dataTadaData.value.name,
    description: dataTadaData.value.description
  })
  .then (GetAllData)
  .then (()=>{
    isEditNewEntity2.value = false
  }) 
}

function SmertLabubi(id: number){
  axios.delete(`/labubu/delete/${id}`)
  .then (GetAllData)
}

watch(searchString,()=>{
  GetAllData()
})


onMounted(()=>{
  GetAllData()
})
</script>