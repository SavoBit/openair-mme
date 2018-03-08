/*
 * Licensed to the OpenAirInterface (OAI) Software Alliance under one or more
 * contributor license agreements.  See the NOTICE file distributed with
 * this work for additional information regarding copyright ownership.
 * The OpenAirInterface Software Alliance licenses this file to You under 
 * the Apache License, Version 2.0  (the "License"); you may not use this file
 * except in compliance with the License.  
 * You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 *-------------------------------------------------------------------------------
 * For more information about the OpenAirInterface (OAI) Software Alliance:
 *      contact@openairinterface.org
 */


#ifndef FILE_MME_APP_STATISTICS_SEEN
#define FILE_MME_APP_STATISTICS_SEEN

#ifdef __cplusplus
extern "C" {
#endif

int mme_app_statistics_display(void);

/*********************************** Utility Functions to update Statistics**************************************/
void update_mme_app_stats_connected_enb_add(void);
void update_mme_app_stats_connected_enb_sub(void);
void update_mme_app_stats_connected_ue_add(void);
void update_mme_app_stats_connected_ue_sub(void);
void update_mme_app_stats_s1u_bearer_add(void);
void update_mme_app_stats_s1u_bearer_sub(void);
void update_mme_app_stats_default_bearer_add(void);
void update_mme_app_stats_default_bearer_sub(void);
void update_mme_app_stats_attached_ue_add(void);
void update_mme_app_stats_attached_ue_sub(void);

#ifdef __cplusplus
}
#endif

#endif /* FILE_MME_APP_STATISTICS_SEEN */
