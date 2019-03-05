export const state = () => ({
    searchFilter: {
        addressOrZip: '',
        searchRadius: 10,
        startDate: new Date(new Date().getFullYear(), new Date().getMonth(),  new Date().getDate()),
        endDate: new Date(new Date().getFullYear(), new Date().getMonth(),  new Date().getDate())
    }
})