<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '@/stores/auth.js';

const success_message = ref('');
const errors = ref([]);
const csrf_token = ref('');
const jwt = localStorage.getItem('jwt');
const router = useRouter();
const authStore = useAuthStore();

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
            // router.push('/');
        }

  }, 3000);
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

onMounted(() => {
    getCsrfToken();
});

function addProfile() {
    const profileForm = document.getElementById('profileForm');
    const formData = new FormData(profileForm);

    success_message.value = '';
    errors.value = [];

    fetch('/api/profiles', {
        method: 'POST',
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
                    router.push("/users");
                }, 3000);
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

<style scoped>
.profile-form-div {
    margin: 0 auto;
    width: 75%;
    padding: 30px;
    border-radius: 20px;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
    background: linear-gradient(135deg, #d1c736, #98d625); /* Green to Gold gradient */
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    color: #000;
}

.profile-form {
    display: flex;
    flex-direction: column;
    gap: 32px;
    margin-top: 20px;
}

.form-group label {
    font-weight: bold;
    font-size: 1rem;
    margin-bottom: 8px;
    color: #fff;
}

input[type="text"],
input[type="number"],
textarea,
select {
    border: 2px solid #1a1a1a;
    border-radius: 10px;
    padding: 10px;
    font-size: 16px;
    background-color: #ffffff;
    color: #000000;
    width: 100%;
}

input:focus,
textarea:focus,
select:focus {
    border-color: #ffb800;
    outline: none;
    box-shadow: 0 0 5px #ffb800;
}

textarea {
    height: 100px;
    resize: vertical;
}

button {
    width: 40%;
    background-color: #000000;
    color: #ffb800;
    padding: 14px 20px;
    border: none;
    border-radius: 12px;
    font-size: 16px;
    font-weight: bold;
    cursor: pointer;
    transition: background-color 0.3s ease, transform 0.2s ease;
}

button:hover {
    background-color: #222222;
    transform: scale(1.05);
}

.success-message {
    background-color: #d4edda;
    color: #155724;
    padding: 12px;
    border-radius: 8px;
    position: fixed;
    top: 80px;
    right: 45px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

.error-message {
    background-color: #f8d7da;
    color: #721c24;
    padding: 16px;
    border-radius: 8px;
    position: fixed;
    top: 80px;
    right: 45px;
    max-width: 350px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

.radio-options,
.group-items,
.fav,
.choices {
    display: flex;
    flex-wrap: wrap;
    gap: 24px;
}

input[type='radio'] {
    margin-right: 8px;
    accent-color: #000;
}

.fade-leave-active {
    transition: opacity 1s ease-in-out;
}

.fade-leave-to {
    opacity: 0;
}

</style>