using UnityEngine;

public class CustomClientStartRequest
{
    public string candidate_1_name { get; set; }
    public string candidate_2_name { get; set; }
}

public class CustomClientChatRequest
{
    public string previous_character_text { get; set; }

    public string previous_speaker { get; set; } // "trump" | "kamala" | "player"
    public string current_speaker { get; set; } // "trump" | "kamala"
}

public class CustomClientChatRawResponse
{
    public string generated_text { get; set; }
    public string audio { get; set; }

    public float anger { get; set; } // 0 - 1
}

public class CustomClientChatResponse : CustomClientChatRawResponse
{
    public AudioClip audioClip { get; set; }
}

public class CustomClientPlayerCardRequest
{
    public string previous_character_text { get; set; }
    public string previous_speaker { get; set; } // "trump" | "kamala" | "player"
    public int card_id { get; set; }
}

public class CustomClientPlayerCardResponseRaw
{
    public string presenter_question { get; set; }
    public string audio { get; set; } // "trump" | "kamala" | "player"
}

public class CustomClientPlayerCardResponse : CustomClientPlayerCardResponseRaw
{
    public AudioClip audioClip { get; set; }
}

public class CustomClientCardsResponse
{
    public DebateCardData[] cards { get; set; }
}
