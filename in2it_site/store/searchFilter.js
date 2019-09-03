export const state = () => ({
    addressOrZip: '60647',
    searchRadius: 3,
    organization: '',
    neighborhood: '',
    startDate: new Date(new Date().getFullYear(), new Date().getMonth(),  new Date().getDate()),
    endDate: new Date(new Date().getFullYear(), new Date().getMonth(),  new Date().getDate() + 7)
})

export const mutations = {
    set (state, data) {
        state.addressOrZip = data.addressOrZip;
        state.searchRadius = data.searchRadius;
        state.organization = data.organization;
        state.neighborhood = data.neighborhood;
        state.startDate = data.startDate;
        state.endDate = data.endDate;
    }
}