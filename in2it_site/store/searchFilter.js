export const state = () => ({
    startTime: new Date(new Date().getFullYear(), new Date().getMonth(),  new Date().getDate()),
    endTime: new Date(new Date().getFullYear(), new Date().getMonth(),  new Date().getDate() + 7),
    miles: 3,
    address: '60647',
    organization: '',
    neighborhood: ''
})

export const mutations = {
    set (state, data) {
        state.startTime = data.startTime;
        state.endTime = data.endTime;
        state.miles = data.miles;
        state.address = data.address;
        state.organization = data.organization;
        state.neighborhood = data.neighborhood;
    }
}