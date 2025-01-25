using UnityEditor;

public class BuildScript
{
    static string[] scenes = { "Assets/Scenes/MainMenu.unity", "Assets/Scenes/MainScene.unity" };

    public static void BuildWebGL()
    {
        BuildPlayerOptions buildPlayerOptions = new BuildPlayerOptions();
        buildPlayerOptions.scenes = scenes;
        buildPlayerOptions.locationPathName = "Builds/WebGL";
        buildPlayerOptions.target = BuildTarget.WebGL;
        buildPlayerOptions.options = BuildOptions.None;
        BuildPipeline.BuildPlayer(buildPlayerOptions);
    }
}
