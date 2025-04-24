<script setup>
import { ref, onMounted } from 'vue'

const success_message = ref('');
const errors = ref([]);

const description = ref('');
const parish = ref('');
const biography = ref('');
const sex = ref('');
const race = ref('');
const birth_year = ref(null);
const height = ref(null);
const fav_cuisine = ref('');
const fav_colour = ref('');
const fav_school_subject = ref('');
const political = ref(null);
const religious = ref(null);
const family_oriented = ref(null);


const togglePoliticalRadioButton = (value) => {
    political.value = political.value === value ? null : value;
}

const toggleReligiousRadioButton = (value) => {
    religious.value = religious.value === value ? null : value;
}

const toggleFamilyOrientedRadioButton = (value) => {
    family_oriented.value = family_oriented.value === value ? null : value;
}

</script>

<template>
    <div class="profile-form-div">

        <h1>Add A New Profile</h1>

        <transition name="fade">
            <div v-if="success_message" class="success-message">
                {{ success_message }}
            </div>
        </transition>


        <transition name="fade">
            <div v-if="errors.length" class="error-message">
                <ul>
                    <li v-for="(error, index) in errors" :key="index">{{ error }}</li>
                </ul>
            </div>
        </transition>

        <form id="profileForm" @submit.prevent="addProfile" class="profile-form" enctype="multipart/form-data">
            <div class="form-group mb-3">
                <label for="description" class="form-label">Description</label>
                <textarea id="description" name="description" v-model="description" class="form-control" ></textarea>
            </div>

            <div class="form-group mb-3">
                <label for="biography" class="form-label">Biography</label>
                <textarea id="biography" name="biography" v-model="biography" class="form-control" ></textarea>
            </div>

            <div class="group-items">
                <div class="form-group mb-3">
                    <label for="parish" class="form-label">Parish</label>
                    <select name="parishes" id="parish" v-model="parish">
                            <option value="">--Select One--</option>
                            <option value="Clarendon">Clarendon</option>
                            <option value="Hanover">Hanover</option>
                            <option value="Kingston">Kingston</option>
                            <option value="Manchester">Manchester</option>
                            <option value="Portland">Portland</option>
                            <option value="St Andrew">St Andrew</option>
                            <option value="St Ann">St Ann</option>
                            <option value="St Catherine">St Catherine</option>
                            <option value="St Elizabeth">St Elizabeth</option>
                            <option value="St James">St James</option>
                            <option value="St Mary">St Mary</option>
                            <option value="St Thomas">St Thomas</option>
                            <option value="Trelawny">Trelawny</option>
                            <option value="Westmoreland">Westmoreland</option>
                    </select>
                </div>

                <div class="form-group mb-3">
                    <label for="sex" class="form-label">Sex</label>
                    <select name="sexes" id="sex" v-model="sex">
                        <option value="">--Select One--</option>
                        <option value="male">Male</option>
                        <option value="female">Female</option>
                    </select>
                </div>

                <div class="form-group mb-3">
                    <label for="race" class="form-label">Race</label>
                    <select name="races" id="race" v-model="race">
                        <option value="">--Select One--</option>
                        <option value="asian">Asian</option>
                        <option value="black">Black</option>
                        <option value="indigenous">Indigenous</option>
                        <option value="mixed">Mixed</option>
                        <option value="white">White</option>
                    </select>
                </div>

                <div class="form-group mb-3">
                    <label for="birth_year" class="form-label">Birth Year</label>
                    <input id="birth_year" type="number" name="birth_year" v-model="birth_year" class="form-control" />
                </div>

                <div class="form-group mb-3">
                    <label for="height" class="form-label">Height</label>
                    <input id="height" type="number" name="height" v-model="height" class="form-control" />
                </div>
            </div>

            <div class="fav">
                <div class="form-group mb-3">
                    <label for="fav_cuisine" class="form-label">Favourite Cuisine</label>
                    <input id="fav_cuisine" type="text" name="fav_cuisine" v-model="fav_cuisine" class="form-control" />
                </div>

                <div class="form-group mb-3">
                    <label for="fav_colour" class="form-label">Favourite Colour</label>
                    <input id="fav_colour" type="text" name="fav_colour" v-model="fav_colour" class="form-control" />
                </div>

                <div class="form-group mb-3">
                    <label for="fav_school_subject" class="form-label">Favourite School Subject</label>
                    <input id="fav_school_subject" type="text" name="fav_school_subject" v-model="fav_school_subject" class="form-control" />
                </div>
            </div>

            <div class="radio-options">
                <div class = "form-group mb3">
                    <label for = "political" class = "form-label">Political</label>
                    <div class="choices">
                        <div>
                            <input id = "political_yes" type = "radio" name = "political" v-model = "political" class = "form-check-input" :value="true" @click = "togglePoliticalRadioButton(true)"/>
                            <label for = "political_yes">Yes</label>
                        </div>
                        
                        <div>
                            <input id = "political_no" type = "radio" name = "political" v-model = "political" class = "form-check-input" :value="false" @click = "togglePoliticalRadioButton(false)"/>
                            <label for = "political_no">No</label>
                        </div>
                    </div>
                </div>
                
                <div class = "form-group mb3">
                    <label for = "religious" class = "form-label">Religious</label>
                    <div class="choices">
                        <div>
                            <input id = "religious_yes" type = "radio" name = "religious" v-model = "religious" class = "form-check-input" :value="true" @click = "toggleReligiousRadioButton(true)"/>
                            <label for = "religious_yes">Yes</label>
                        </div>
                        
                        <div>
                            <input id = "religious_no" type = "radio" name = "religious" v-model = "religious" class = "form-check-input" :value="false" @click = "toggleReligiousRadioButton(false)"/>
                            <label for = "religious_no">No</label>
                        </div>
                    </div>
                    
                </div>

                <div class = "form-group mb3">
                    <label for = "family_oriented" class = "form-label">Family Oriented</label>
                    <div class="choices">
                        <div>
                            <input id = "family_oriented_yes" type = "radio" name = "family_oriented" v-model = "family_oriented" class = "form-check-input" :value="true" @click = "toggleFamilyOrientedRadioButton(true)"/>
                            <label for = "family_oriented_yes">Yes</label>
                        </div>
                        
                        <div>
                            <input id = "family_oriented_no" type = "radio" name = "family_oriented" v-model = "family_oriented" class = "form-check-input" :value="false" @click = "toggleFamilyOrientedRadioButton(false)"/>
                            <label for = "family_oriented_no">No</label>
                        </div>
                    </div>
                </div>
            </div>

            <button type="submit" name="submit" class="btn btn-primary">Submit</button>
        </form>

    </div>

</template>


<style scoped>

.profile-form-div {
    margin: 0 auto;
    width: 75%;
    padding: 20px;
    border: 1px solid #ccc;
    border-radius: 5px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    background-color: #f9f9f9;
}

.profile-form {
    display: flex;
    flex-direction: column;
    gap: 30px;
    margin-top: 30px;
}

.form-group {
    margin-bottom: 15px;
}

.group-items {
    display: flex;
    flex-direction: row;
    justify-content: space-between;
}

.fav {
    display: flex;
    flex-direction: row;
    justify-content: left;
    gap: 222px;
}

.radio-options {
    display: flex;
    flex-direction: row;
    justify-content: left;
    gap: 222px;
}

.choices {
    display: flex;
    flex-direction: row;
    justify-content: center;
    gap: 20px;
}

div select {
    display: flex;
    flex-direction: column;
}

input[id^='fav'] {
    width: 140%;
}

input[id^='pol'], input[id^='rel'], input[id^='fam'] {
    margin-right: 10px;
}

input {
    border: 1px solid #ccc;
    border-radius: 8px;
}

button {
    width: 10%;
}

textarea {
    width: 100%;
    height: 100px;
    resize: none;
    border-radius: 8px;
    border: 1px solid #ccc;
}

select { background-color: #fff;
  border: 1px solid #ccc;
  border-radius: 8px;
  padding: 8px 20px 5px 12px;
  font-size: 14px;
  cursor: pointer;
  height: 38px;
  }
</style>