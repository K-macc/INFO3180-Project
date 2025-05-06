<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '@/stores/auth';

const success_message = ref('');
const errors = ref([]);
const csrf_token = ref('');
const router = useRouter();
const authStore = useAuthStore();
const profileID = authStore.profile_id;
const profile = ref(null);


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

function flashMessage(prompt) {
    setTimeout(() => {
        if (Array.isArray(prompt)) {
            prompt.value = [];
        } else {
            prompt.value = '';
        }
    }, 3000);
}

function preFillForm() {
    description.value = profile.value.description;
    parish.value = profile.value.parish;
    biography.value = profile.value.biography;
    sex.value = profile.value.sex;
    race.value = profile.value.race;
    birth_year.value = profile.value.birth_year;
    height.value = profile.value.height;
    fav_cuisine.value = profile.value.fav_cuisine;
    fav_colour.value = profile.value.fav_colour;
    fav_school_subject.value = profile.value.fav_school_subject;
    political.value = profile.value.political;
    religious.value = profile.value.religious;
    family_oriented.value = profile.value.family_oriented;
}


function getCsrfToken() {
    fetch('/api/v1/csrf-token')
        .then((response) => response.json())
        .then((data) => {
            csrf_token.value = data.csrf_token;
        })
        .catch((error) => {
            console.error("Error: ", error);
        });
}

function fetchProfile() {
    fetch(`/api/profiles/${profileID}`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${authStore.token}`
        }
    })
        .then(response => {
            return response.json();
        })
        .then(data => {
            if (data.error) {
                console.error('Error fetching profile:', data.error);
                return;
            } else {
                profile.value = data.profile;
                preFillForm();
            }
        })
        .catch(error => {
            console.error('Failed to parse JSON:', error);
        })

}

onMounted(() => {
    fetchProfile();
    getCsrfToken();
});

function updateProfile() {
    const profileForm = document.getElementById('profileForm');
    const formData = new FormData(profileForm);

    success_message.value = '';
    errors.value = [];

    fetch(`/api/profiles/${profileID}`, {
        method: 'PUT',
        body: formData,
        credentials: 'include',
        headers: {
            'Authorization': `Bearer ${authStore.token}`,
            'X-CSRF-Token': csrf_token.value
        }
    })
        .then(response => response.json())
        .then(data => {
            if (data.message) {
                success_message.value = data.message;
                flashMessage(success_message);
                profileForm.reset();
                setTimeout(() => {
                    router.push('/users');
                }, 4000);
            } else if (data.error) {
                errors.value.push(data.error);
                flashMessage(errors);
            } else {
                errors.value = data.errors;
                flashMessage(errors);
            }
        })
        .catch(error => {
            console.error('Failed to parse JSON:', error);
            errors.value.push('An error occurred while processing your request.');
            flashMessage(errors);
        });

}
</script>

<template>
    <div class="profile-form-div">

        <h1>Update Your Profile</h1>

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

        <form id="profileForm" @submit.prevent="updateProfile" class="profile-form" enctype="multipart/form-data">
            <div class="form-group mb-3">
                <label for="description" class="form-label">Description</label>
                <textarea id="description" name="description" v-model="description" class="form-control"></textarea>
            </div>

            <div class="form-group mb-3">
                <label for="biography" class="form-label">Biography</label>
                <textarea id="biography" name="biography" v-model="biography" class="form-control"></textarea>
            </div>

            <div class="group-items">
                <div class="form-group mb-3">
                    <label for="parish" class="form-label">Parish</label>
                    <select name="parish" id="parish" v-model="parish">
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
                    <select name="sex" id="sex" v-model="sex">
                        <option value="">--Select One--</option>
                        <option value="male">Male</option>
                        <option value="female">Female</option>
                    </select>
                </div>

                <div class="form-group mb-3">
                    <label for="race" class="form-label">Race</label>
                    <select name="race" id="race" v-model="race">
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
                    <input id="fav_school_subject" type="text" name="fav_school_subject" v-model="fav_school_subject"
                        class="form-control" />
                </div>
            </div>

            <div class="radio-options">
                <div class="form-group mb3">
                    <label for="political" class="form-label">Political</label>
                    <div class="choices">
                        <div>
                            <input id="political_yes" type="radio" name="political" v-model="political"
                                class="form-check-input" :value="true" @click="togglePoliticalRadioButton(true)" />
                            <label for="political_yes">Yes</label>
                        </div>

                        <div>
                            <input id="political_no" type="radio" name="political" v-model="political"
                                class="form-check-input" :value="false" @click="togglePoliticalRadioButton(false)" />
                            <label for="political_no">No</label>
                        </div>
                    </div>
                </div>

                <div class="form-group mb3">
                    <label for="religious" class="form-label">Religious</label>
                    <div class="choices">
                        <div>
                            <input id="religious_yes" type="radio" name="religious" v-model="religious"
                                class="form-check-input" :value="true" @click="toggleReligiousRadioButton(true)" />
                            <label for="religious_yes">Yes</label>
                        </div>

                        <div>
                            <input id="religious_no" type="radio" name="religious" v-model="religious"
                                class="form-check-input" :value="false" @click="toggleReligiousRadioButton(false)" />
                            <label for="religious_no">No</label>
                        </div>
                    </div>

                </div>

                <div class="form-group mb3">
                    <label for="family_oriented" class="form-label">Family Oriented</label>
                    <div class="choices">
                        <div>
                            <input id="family_oriented_yes" type="radio" name="family_oriented"
                                v-model="family_oriented" class="form-check-input" :value="true"
                                @click="toggleFamilyOrientedRadioButton(true)" />
                            <label for="family_oriented_yes">Yes</label>
                        </div>

                        <div>
                            <input id="family_oriented_no" type="radio" name="family_oriented" v-model="family_oriented"
                                class="form-check-input" :value="false"
                                @click="toggleFamilyOrientedRadioButton(false)" />
                            <label for="family_oriented_no">No</label>
                        </div>
                    </div>
                </div>
            </div>

            <button type="submit" name="submit" class="btn btn-primary">Submit</button>
        </form>

    </div>

</template>

<style>
.profile-form-div {
    margin: 30px auto;
    width: 75%;
    background: linear-gradient(135deg, #9cb62a, #d2e434);
    /* Green to Gold gradient */
    padding: 20px;
    border: 1px solid #ddd;
    color: white;
    border-radius: 10px;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.08);
}

h1 {
    text-align: center;
    color: #2c3e50;
    font-size: 2rem;
}

.profile-form {
    display: flex;
    flex-direction: column;
    gap: 30px;
    color: white;
    margin-top: 30px;
}

.form-label {
    font-weight: 600;
    color: #34495e;
}

input,
textarea,
select {
    border: 1px solid #ccc;
    border-radius: 8px;
    padding: 10px;
    font-size: 14px;
    background-color: #fdfdfd;
    color: #2c3e50;
}

textarea {
    height: 100px;
    resize: none;
}

button {
    background-color: #3498db;
    color: white;
    padding: 10px 20px;
    border: none;
    border-radius: 8px;
    font-size: 16px;
    cursor: pointer;
    transition: background-color 0.3s ease;
    width: 150px;
    align-self: center;
}

button:hover {
    background-color: #2980b9;
}

.group-items,
.fav,
.radio-options {
    display: flex;
    flex-wrap: wrap;
    gap: 30px;
}

input[id^='fav'],
input[id^='pol'],
input[id^='rel'],
input[id^='fam'] {
    margin-right: 10px;
}

.success-message {
    color: #155724;
    background-color: #d4edda;
    padding: 10px;
    border-radius: 8px;
    border: 1px solid #c3e6cb;
    text-align: center;
    position: fixed;
    top: 100px;
    right: 45px;
    width: 250px;
    z-index: 1000;
    box-shadow: 0 2px 8px rgba(0, 128, 0, 0.2);
}

.error-message {
    color: #721c24;
    background-color: #f8d7da;
    padding: 12px;
    border-radius: 8px;
    border: 1px solid #f5c6cb;
    position: fixed;
    top: 70px;
    right: 45px;
    width: 300px;
    z-index: 1000;
    box-shadow: 0 2px 8px rgba(255, 0, 0, 0.2);
}

.fade-leave-active {
    transition: opacity 1s ease-in-out;
}

.fade-leave-to {
    opacity: 0;
}

select {
    appearance: none;
    background-color: #fff;
    background-image: url('data:image/svg+xml;charset=US-ASCII,<svg xmlns="http://www.w3.org/2000/svg" width="14" height="10"><polygon points="7,10 0,0 14,0" style="fill:%233498db"/></svg>');
    background-repeat: no-repeat;
    background-position: right 10px center;
    background-size: 12px;
}
</style>
