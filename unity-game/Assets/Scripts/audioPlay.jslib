// Place this in a .jslib file in your Unity project
var AudioPlayer = {
    PlayMP3FromBase64: function (base64String) {
        var audio = new Audio("data:audio/mp3;base64," + base64String);
        audio.play();
    }
};
mergeInto(LibraryManager.library, AudioPlayer);
