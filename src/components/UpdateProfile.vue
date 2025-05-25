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
const height = ref('');
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
        .then(response => response.json())
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
    <div class="profile-form-bg">
        <div class="profile-form-card">
            <h1>Update Your Profile</h1>

            <transition name="fade">
                <div v-if="success_message" class="alert success-message">
                    {{ success_message }}
                </div>
            </transition>
            <transition name="fade">
                <div v-if="errors.length" class="alert error-message">
                    <ul>
                        <li v-for="(error, index) in errors" :key="index">{{ error }}</li>
                    </ul>
                </div>
            </transition>

            <form id="profileForm" @submit.prevent="updateProfile" class="profile-form" enctype="multipart/form-data">
                <div class="form-section">
                    <label for="description" class="form-label">Description</label>
                    <textarea id="description" name="description" v-model="description" class="form-control"></textarea>
                </div>

                <div class="form-section">
                    <label for="biography" class="form-label">Biography</label>
                    <textarea id="biography" name="biography" v-model="biography" class="form-control"></textarea>
                </div>

                <div class="form-row">
                    <div class="form-section">
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
                    <div class="form-section">
                        <label for="sex" class="form-label">Sex</label>
                        <select name="sex" id="sex" v-model="sex">
                            <option value="">--Select One--</option>
                            <option value="male">Male</option>
                            <option value="female">Female</option>
                        </select>
                    </div>
                    <div class="form-section">
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
                </div>

                <div class="form-row">
                    <div class="form-section">
                        <label for="birth_year" class="form-label">Birth Year</label>
                        <input id="birth_year" type="number" name="birth_year" v-model="birth_year"
                            class="form-control" />
                    </div>
                    <div class="form-section">
                        <label for="height" class="form-label">Height (ft in)</label>
                        <input id="height" type="text" name="height" v-model="height" class="form-control" placeholder="eg (5'11)"/>
                    </div>
                </div>

                <div class="form-row">
                    <div class="form-section">
                        <label for="fav_cuisine" class="form-label">Favourite Cuisine</label>
                        <input id="fav_cuisine" type="text" name="fav_cuisine" v-model="fav_cuisine"
                            class="form-control" />
                    </div>
                    <div class="form-section">
                        <label for="fav_colour" class="form-label">Favourite Colour</label>
                        <input id="fav_colour" type="text" name="fav_colour" v-model="fav_colour"
                            class="form-control" />
                    </div>
                    <div class="form-section">
                        <label for="fav_school_subject" class="form-label">Favourite School Subject</label>
                        <input id="fav_school_subject" type="text" name="fav_school_subject"
                            v-model="fav_school_subject" class="form-control" />
                    </div>
                </div>

                <div class="form-row radio-row">
                    <div class="form-section">
                        <label class="form-label">Political</label>
                        <div class="radio-group">
                            <label>
                                <input type="radio" name="political" v-model="political" :value="true"
                                    @click="togglePoliticalRadioButton(true)" />
                                Yes
                            </label>
                            <label>
                                <input type="radio" name="political" v-model="political" :value="false"
                                    @click="togglePoliticalRadioButton(false)" />
                                No
                            </label>
                        </div>
                    </div>
                    <div class="form-section">
                        <label class="form-label">Religious</label>
                        <div class="radio-group">
                            <label>
                                <input type="radio" name="religious" v-model="religious" :value="true"
                                    @click="toggleReligiousRadioButton(true)" />
                                Yes
                            </label>
                            <label>
                                <input type="radio" name="religious" v-model="religious" :value="false"
                                    @click="toggleReligiousRadioButton(false)" />
                                No
                            </label>
                        </div>
                    </div>
                    <div class="form-section">
                        <label class="form-label">Family Oriented</label>
                        <div class="radio-group">
                            <label>
                                <input type="radio" name="family_oriented" v-model="family_oriented" :value="true"
                                    @click="toggleFamilyOrientedRadioButton(true)" />
                                Yes
                            </label>
                            <label>
                                <input type="radio" name="family_oriented" v-model="family_oriented" :value="false"
                                    @click="toggleFamilyOrientedRadioButton(false)" />
                                No
                            </label>
                        </div>
                    </div>
                </div>

                <div class="form-actions">
                    <button type="submit" name="submit" class="btn btn-primary">Update</button>
                </div>
            </form>
        </div>
    </div>
</template>

<style scoped>
.profile-form-bg {
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 2rem 0;
}

.profile-form-card {
    background: #fff;
    border-radius: 2rem;
    box-shadow: 0 12px 36px rgba(138, 0, 71, 0.12), 0 1.5px 6px rgba(0, 0, 0, 0.04);
    padding: 2.5rem 2rem 2rem 2rem;
    max-width: 800px;
    width: 100%;
    margin: 0 1rem;
    display: flex;
    flex-direction: column;
    gap: 2rem;
    animation: fadeIn 0.8s cubic-bezier(.68, -0.55, .27, 1.55);
}


h1 {
    color: #8a0047;
    text-align: center;
    font-size: 2.2rem;
    font-weight: 700;
    margin-bottom: 1rem;
    letter-spacing: 1px;
}

.profile-form {
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
}

.form-section {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
    flex: 1;
}

.form-row {
    display: flex;
    gap: 1.2rem;
    flex-wrap: wrap;
}

.radio-row {
    align-items: flex-end;
}

.form-label {
    font-weight: 600;
    font-size: 1rem;
    color: #8a0047;
}

input[type="text"],
input[type="number"],
textarea,
select {
    border: 2px solid #ad2874;
    border-radius: 10px;
    padding: 10px;
    font-size: 16px;
    background-color: #faf8fa;
    color: #333333;
    width: 100%;
    transition: border-color 0.3s, box-shadow 0.3s;
}

input:focus,
textarea:focus,
select:focus {
    border-color: #00c8ff;
    outline: none;
    box-shadow: 0 0 6px #00c8ff33;
}

textarea {
    min-height: 80px;
    resize: vertical;
}

.radio-group {
    display: flex;
    gap: 1.2rem;
    margin-top: 0.2rem;
    color: #8a0047;
}

input[type='radio'] {
    margin-right: 6px;
    accent-color: #ad2874;
}

.btn {
    padding: 0.75rem 2rem;
    border-radius: 0.7rem;
    font-weight: 600;
    font-size: 1.1rem;
    cursor: pointer;
    border: none;
    color: #fff;
    transition: background 0.3s, color 0.3s;
    box-shadow: 0 2px 8px rgba(138, 0, 71, 0.07);
}

.btn:hover {
    transform: translateY(-2px);
    color: #fff;
}

.form-actions {
    display: flex;
    justify-content: center;
    margin-top: 1rem;
}

.success-message {
    position: fixed;
    top: 130px;
    right: 160px;
    padding: 1rem 1.5rem;
    border-radius: 0.7rem;
    font-weight: 500;
    z-index: 1100;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.08);
    font-size: 1.1rem;
    display: flex;
    align-items: center;
    gap: 0.75rem;
    text-align: left;
}

.error-message {
    position: fixed;
    top: 80px;
    right: 10px;
    padding: 1rem 1.5rem;
    border-radius: 0.7rem;
    font-weight: 500;
    z-index: 1000;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.08);
    font-size: 1.1rem;
    max-width: 650px;
    display: flex;
    align-items: center;
    gap: 0.75rem;
    text-align: left;
}

.error-message * {
    margin: 0;
}

.success-message {
    background-color: #d0f5e8;
    color: #0C4A6E;
}

.error-message {
    background-color: #fde8ef;
    color: #8a0047;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
