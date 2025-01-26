// using System;
// using System.IO;
// using FMOD;
// using FMODUnity;
// using UnityEngine;

// public static class AudioConverter
// {
//     public static FMOD.Sound ConvertMp3StreamToFmodSound(byte[] mp3Bytes, out FMOD.RESULT result)
//     {
//         try
//         {
//             // Initialiser le système FMOD
//             FMOD.System system;
//             result = FMODUnity.RuntimeManager.CoreSystem.getCoreSystem(out system);
//             if (result != FMOD.RESULT.OK)
//             {
//                 Debug.LogError($"Erreur lors de l'initialisation du système FMOD : {result}");
//                 return null;
//             }

//             // Créer un flux audio à partir des données MP3
//             FMOD.CREATESOUNDEXINFO soundInfo = new FMOD.CREATESOUNDEXINFO();
//             soundInfo.cbsize = System.Runtime.InteropServices.Marshal.SizeOf(
//                 typeof(FMOD.CREATESOUNDEXINFO)
//             );
//             soundInfo.length = (uint)mp3Bytes.Length;

//             // Créer un son à partir des données brutes MP3
//             FMOD.Sound sound;
//             result = system.createSound(
//                 mp3Bytes,
//                 FMOD.MODE.CREATESTREAM | FMOD.MODE.LOOP_OFF,
//                 ref soundInfo,
//                 out sound
//             );
//             if (result != FMOD.RESULT.OK)
//             {
//                 Debug.LogError($"Erreur lors de la création du son FMOD : {result}");
//                 return null;
//             }

//             // Obtenir des informations sur le son
//             int sampleRate,
//                 channels;
//             FMOD.SOUND_FORMAT format;
//             result = sound.getFormat(out _, out format, out channels, out _);
//             result = sound.getDefaults(out sampleRate, out _);

//             if (result != FMOD.RESULT.OK)
//             {
//                 Debug.LogError($"Erreur lors de l'obtention des informations du son : {result}");
//                 return null;
//             }

//             Debug.Log(
//                 $"FMOD Sound Loaded: Sample Rate = {sampleRate}, Channels = {channels}, Format = {format}"
//             );

//             return sound;
//         }
//         catch (Exception ex)
//         {
//             Debug.LogError($"Erreur lors de la conversion du flux MP3 avec FMOD : {ex.Message}");
//             result = FMOD.RESULT.ERR_INTERNAL;
//             return null;
//         }
//     }
// }
