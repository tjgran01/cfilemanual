survey_strings = {"tlx": ("NASA - TLX Please fill out the following survey "
                          "items to reflect your experience during the "
                          "task..."),
                  "mrq": ("MRQ - "),
                  "empathy": ("Please take a look at the following picture, "
                              "and answer the questionnaire. Take enough time "
                              "to un..."),
                  "soyoung_media": ("some string")
                 }

survey_dict = {"phys_info": ["", "onset", "duration", "stim"],

               "tlx": ["tlx", "tlx_mental", "tlx_physical",
                        "tlx_temporal", "tlx_performance",
                        "tlx_effort", "tlx_frustration"],

               "mrq": ["", "onset", "duration", "stim", "mrq"],
               "empathy": ["emp_prompt", "emp_pic", "emp_how_feel",
                           "emp_concern", "emp_aroused", "emp_touching"],
               "soyoung_media": ["", ""],
              }

templates = {"soyoung": ["", "onset", "duration", "stim",
                         'Empathy1', 'Empathy2', 'Empathy3', 'Empathy4',
                         'Recall_1', 'Recall_2', 'Source_credibility1',
                         'Source_credibility2', 'Source_credibility3',
                         'Source_credibility4', 'Source_credibility5',
                         'Behavior_Intention1', 'Behavior_Intention2',
                         'Behavior_Intention3', 'SP1', 'SP2', 'SP3', 'SP4',
                         'SP5', 'SP6', 'PSI_1', 'PSI_2', 'PSI_3', 'PSI_4',
                         'PSI_5', 'PSI_6', 'PSI_7', 'Presence1', 'Presence2',
                         'Presence3', 'Presence4', 'Presence5', 'Presence6',
                         'Presence7', 'Presence8', 'Presence9', 'Presence10',
                         'Presence11', 'Adj_SP1', 'Adj_SP2', 'Adj_SP3',
                         'Adj_SP4', 'Adj_SP5', 'Adj_SP6',
                         'Adj_SP_cog1', 'Adj_SP_cog2', 'Adj_SP_cog3',
                         'HealthConcern1', 'HealthConcern2', 'HealthConcern3',
                         'HealthConcern4', 'HealthConcern5', 'Content_affective1',
                         'Content_Cog1', 'Content_Cog2', 'Content_Cog3',
                         'Content_affective2', 'Content_affective3',
                         'Content_affective4']
             }
