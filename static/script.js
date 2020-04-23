// VueJS
var vm = new Vue({
    el: "#vue-app",
    data: function () {
        return {
            albums_url: "/static/data/albums.json",
            albums: [],
            modalAlbum: {}
        }
    },
    created() {
        fetch(this.albums_url)
            .then(response => response.json())
            .then(json => {
                this.albums = json.albums;
                $(function () {
                    $('[data-toggle="tooltip"]').tooltip()
                })
            });
    },
    methods: {
        setModalData: function (album) {
            this.modalAlbum = album;
        },
        parseTimestamp: function (timestamp) {
            let date = new Date(timestamp * 1000);
            return date.toLocaleString();
        }
    }
})
