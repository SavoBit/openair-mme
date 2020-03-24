#/*
# * Licensed to the OpenAirInterface (OAI) Software Alliance under one or more
# * contributor license agreements.  See the NOTICE file distributed with
# * this work for additional information regarding copyright ownership.
# * The OpenAirInterface Software Alliance licenses this file to You under
# * the OAI Public License, Version 1.1  (the "License"); you may not use this file
# * except in compliance with the License.
# * You may obtain a copy of the License at
# *
# *	  http://www.openairinterface.org/?page_id=698
# *
# * Unless required by applicable law or agreed to in writing, software
# * distributed under the License is distributed on an "AS IS" BASIS,
# * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# * See the License for the specific language governing permissions and
# * limitations under the License.
# *-------------------------------------------------------------------------------
# * For more information about the OpenAirInterface (OAI) Software Alliance:
# *	  contact@openairinterface.org
# */
#---------------------------------------------------------------------

import os
import re
import sys

class mmeConfigGen():
	def __init__(self):
		self.kind = ''
		self.hss_s6a_IP = ''
		self.mme_s6a_IP = ''
		self.mme_s1c_IP = ''
		self.mme_s1c_name = ''
		self.mme_s10_IP = ''
		self.mme_s10_name = ''
		self.mme_s11_IP = ''
		self.mme_s11_name = ''
		self.spgwc0_s11_IP = ''
		self.fromDockerFile = False

	def GenerateMMEConfigurer(self):
		mmeFile = open('./mme-cfg.sh', 'w')
		mmeFile.write('#!/bin/bash\n')
		mmeFile.write('\n')
		if self.fromDockerFile:
			mmeFile.write('cd /openair-mme/scripts\n')
		else:
			mmeFile.write('cd /home/scripts\n')
		mmeFile.write('\n')
		mmeFile.write('INSTANCE=1\n')
		if self.fromDockerFile:
			mmeFile.write('PREFIX=\'/openair-mme/etc\'\n')
		else:
			mmeFile.write('PREFIX=\'/usr/local/etc/oai\'\n')
		# The following variables could be later be passed as parameters
		mmeFile.write('MY_REALM=\'openairinterface.org\'\n')
		mmeFile.write('\n')
		if not self.fromDockerFile:
			mmeFile.write('rm -Rf $PREFIX\n')
			mmeFile.write('\n')
			mmeFile.write('mkdir -p $PREFIX\n')
			mmeFile.write('mkdir $PREFIX/freeDiameter\n')
			mmeFile.write('\n')
			mmeFile.write('cp ../etc/mme_fd.sprint.conf $PREFIX/freeDiameter/mme_fd.conf\n')
			mmeFile.write('cp ../etc/mme.conf  $PREFIX\n')
			mmeFile.write('\n')
		mmeFile.write('declare -A MME_CONF\n')
		mmeFile.write('\n')
		mmeFile.write('MME_CONF[@MME_S6A_IP_ADDR@]="' + self.mme_s6a_IP + '"\n')
		mmeFile.write('MME_CONF[@INSTANCE@]=$INSTANCE\n')
		mmeFile.write('MME_CONF[@PREFIX@]=$PREFIX\n')
		mmeFile.write('MME_CONF[@REALM@]=$MY_REALM\n')
		mmeFile.write('MME_CONF[@PID_DIRECTORY@]=\'/var/run\'\n')
		mmeFile.write('MME_CONF[@MME_FQDN@]="mme.${MME_CONF[@REALM@]}"\n')
		mmeFile.write('MME_CONF[@HSS_HOSTNAME@]=\'hss\'\n')
		mmeFile.write('MME_CONF[@HSS_FQDN@]="${MME_CONF[@HSS_HOSTNAME@]}.${MME_CONF[@REALM@]}"\n')
		mmeFile.write('MME_CONF[@HSS_IP_ADDR@]="' + self.hss_s6a_IP + '"\n')
		mmeFile.write('MME_CONF[@MCC@]=\'208\'\n')
		mmeFile.write('MME_CONF[@MNC@]=\'93\'\n')
		mmeFile.write('MME_CONF[@MME_GID@]=\'32768\'\n')
		mmeFile.write('MME_CONF[@MME_CODE@]=\'3\'\n')
		mmeFile.write('MME_CONF[@TAC_0@]=\'600\'\n')
		mmeFile.write('MME_CONF[@TAC_1@]=\'601\'\n')
		mmeFile.write('MME_CONF[@TAC_2@]=\'602\'\n')
		mmeFile.write('MME_CONF[@MME_INTERFACE_NAME_FOR_S1_MME@]=\'' + self.mme_s1c_name + '\'\n')
		mmeFile.write('MME_CONF[@MME_IPV4_ADDRESS_FOR_S1_MME@]=\'' + self.mme_s1c_IP + '/24\'\n')
		mmeFile.write('MME_CONF[@MME_INTERFACE_NAME_FOR_S11@]=\'' + self.mme_s11_name + '\'\n')
		mmeFile.write('MME_CONF[@MME_IPV4_ADDRESS_FOR_S11@]=\'' + self.mme_s11_IP + '/24\'\n')
		mmeFile.write('MME_CONF[@MME_INTERFACE_NAME_FOR_S10@]=\'' + self.mme_s10_name + '\'\n')
		mmeFile.write('MME_CONF[@MME_IPV4_ADDRESS_FOR_S10@]=\'' + self.mme_s10_IP + '/24\'\n')
		mmeFile.write('MME_CONF[@OUTPUT@]=\'CONSOLE\'\n')
		mmeFile.write('MME_CONF[@SGW_IPV4_ADDRESS_FOR_S11_0@]=\'' + self.spgwc0_s11_IP + '\'\n')
		mmeFile.write('MME_CONF[@PEER_MME_IPV4_ADDRESS_FOR_S10_0@]=\'0.0.0.0/24\'\n')
		mmeFile.write('MME_CONF[@PEER_MME_IPV4_ADDRESS_FOR_S10_1@]=\'0.0.0.0/24\'\n')
		mmeFile.write('\n')
		mmeFile.write('TAC_SGW_TEST=\'7\'\n')
		mmeFile.write('tmph=`echo "$TAC_SGW_TEST / 256" | bc`\n')
		mmeFile.write('tmpl=`echo "$TAC_SGW_TEST % 256" | bc`\n')
		mmeFile.write('MME_CONF[@TAC-LB_SGW_TEST_0@]=`printf "%02x\\n" $tmpl`\n')
		mmeFile.write('MME_CONF[@TAC-HB_SGW_TEST_0@]=`printf "%02x\\n" $tmph`\n')
		mmeFile.write('\n')
		mmeFile.write('MME_CONF[@MCC_SGW_0@]=${MME_CONF[@MCC@]}\n')
		mmeFile.write('MME_CONF[@MNC3_SGW_0@]=`printf "%03d\\n" $(echo ${MME_CONF[@MNC@]} | sed -e "s/^0*//")`\n')
		mmeFile.write('TAC_SGW_0=\'600\'\n')
		mmeFile.write('tmph=`echo "$TAC_SGW_0 / 256" | bc`\n')
		mmeFile.write('tmpl=`echo "$TAC_SGW_0 % 256" | bc`\n')
		mmeFile.write('MME_CONF[@TAC-LB_SGW_0@]=`printf "%02x\\n" $tmpl`\n')
		mmeFile.write('MME_CONF[@TAC-HB_SGW_0@]=`printf "%02x\\n" $tmph`\n')
		mmeFile.write('\n')
		mmeFile.write('MME_CONF[@MCC_MME_0@]=${MME_CONF[@MCC@]}\n')
		mmeFile.write('MME_CONF[@MNC3_MME_0@]=`printf "%03d\\n" $(echo ${MME_CONF[@MNC@]} | sed -e "s/^0*//")`\n')
		mmeFile.write('TAC_MME_0=\'601\'\n')
		mmeFile.write('tmph=`echo "$TAC_MME_0 / 256" | bc`\n')
		mmeFile.write('tmpl=`echo "$TAC_MME_0 % 256" | bc`\n')
		mmeFile.write('MME_CONF[@TAC-LB_MME_0@]=`printf "%02x\\n" $tmpl`\n')
		mmeFile.write('MME_CONF[@TAC-HB_MME_0@]=`printf "%02x\\n" $tmph`\n')
		mmeFile.write('\n')
		mmeFile.write('MME_CONF[@MCC_MME_1@]=${MME_CONF[@MCC@]}\n')
		mmeFile.write('MME_CONF[@MNC3_MME_1@]=`printf "%03d\\n" $(echo ${MME_CONF[@MNC@]} | sed -e "s/^0*//")`\n')
		mmeFile.write('TAC_MME_1=\'602\'\n')
		mmeFile.write('tmph=`echo "$TAC_MME_1 / 256" | bc`\n')
		mmeFile.write('tmpl=`echo "$TAC_MME_1 % 256" | bc`\n')
		mmeFile.write('MME_CONF[@TAC-LB_MME_1@]=`printf "%02x\\n" $tmpl`\n')
		mmeFile.write('MME_CONF[@TAC-HB_MME_1@]=`printf "%02x\\n" $tmph`\n')
		mmeFile.write('\n')
		mmeFile.write('for K in "${!MME_CONF[@]}"; do \n')
		mmeFile.write('  egrep -lRZ "$K" $PREFIX | xargs -0 -l sed -i -e "s|$K|${MME_CONF[$K]}|g"\n')
		mmeFile.write('  ret=$?;[[ ret -ne 0 ]] && echo "Tried to replace $K with ${MME_CONF[$K]}"\n')
		mmeFile.write('done\n')
		mmeFile.write('\n')
		mmeFile.write('# Generate freeDiameter certificate\n')
		if self.fromDockerFile:
			mmeFile.write('./check_mme_s6a_certificate $PREFIX mme.${MME_CONF[@REALM@]}\n')
		else:
			mmeFile.write('./check_mme_s6a_certificate $PREFIX/freeDiameter mme.${MME_CONF[@REALM@]}\n')
		mmeFile.close()

#-----------------------------------------------------------
# Usage()
#-----------------------------------------------------------
def Usage():
	print('----------------------------------------------------------------------------------------------------------------------')
	print('generateConfigFiles.py')
	print('   Prepare a bash script to be run in the workspace where MME is being built.')
	print('   That bash script will copy configuration template files and adapt to your configuration.')
	print('----------------------------------------------------------------------------------------------------------------------')
	print('Usage: python3 generateConfigFiles.py [options]')
	print('  --help  Show this help.')
	print('---------------------------------------------------------------------------------------------------- HSS Options -----')
	print('  --kind=MME')
	print('  --hss_s6a=[HSS S6A Interface IP server]')
	print('  --mme_s6a=[MME S6A Interface IP server]')
	print('  --mme_s1c_IP=[MME S1-C Interface IP address]')
	print('  --mme_s1c_name=[MME S1-C Interface name]')
	print('  --mme_s10_IP=[MME S10 Interface IP address]')
	print('  --mme_s10_name=[MME S10 Interface name]')
	print('  --mme_s11_IP=[MME S11 Interface IP address]')
	print('  --mme_s11_name=[MME S11 Interface name]')
	print('  --spgwc0_s11_IP=[SPGW-C Instance 0 - S11 Interface IP address]')
	print('  --from_docker_file')

argvs = sys.argv
argc = len(argvs)
cwd = os.getcwd()

myMME = mmeConfigGen()

while len(argvs) > 1:
	myArgv = argvs.pop(1)
	if re.match('^\-\-help$', myArgv, re.IGNORECASE):
		Usage()
		sys.exit(0)
	elif re.match('^\-\-kind=(.+)$', myArgv, re.IGNORECASE):
		matchReg = re.match('^\-\-kind=(.+)$', myArgv, re.IGNORECASE)
		myMME.kind = matchReg.group(1)
	elif re.match('^\-\-hss_s6a=(.+)$', myArgv, re.IGNORECASE):
		matchReg = re.match('^\-\-hss_s6a=(.+)$', myArgv, re.IGNORECASE)
		myMME.hss_s6a_IP = matchReg.group(1)
	elif re.match('^\-\-mme_s6a=(.+)$', myArgv, re.IGNORECASE):
		matchReg = re.match('^\-\-mme_s6a=(.+)$', myArgv, re.IGNORECASE)
		myMME.mme_s6a_IP = matchReg.group(1)
	elif re.match('^\-\-mme_s1c_IP=(.+)$', myArgv, re.IGNORECASE):
		matchReg = re.match('^\-\-mme_s1c_IP=(.+)$', myArgv, re.IGNORECASE)
		myMME.mme_s1c_IP = matchReg.group(1)
	elif re.match('^\-\-mme_s1c_name=(.+)$', myArgv, re.IGNORECASE):
		matchReg = re.match('^\-\-mme_s1c_name=(.+)$', myArgv, re.IGNORECASE)
		myMME.mme_s1c_name = matchReg.group(1)
	elif re.match('^\-\-mme_s10_IP=(.+)$', myArgv, re.IGNORECASE):
		matchReg = re.match('^\-\-mme_s10_IP=(.+)$', myArgv, re.IGNORECASE)
		myMME.mme_s10_IP = matchReg.group(1)
	elif re.match('^\-\-mme_s10_name=(.+)$', myArgv, re.IGNORECASE):
		matchReg = re.match('^\-\-mme_s10_name=(.+)$', myArgv, re.IGNORECASE)
		myMME.mme_s10_name = matchReg.group(1)
	elif re.match('^\-\-mme_s11_IP=(.+)$', myArgv, re.IGNORECASE):
		matchReg = re.match('^\-\-mme_s11_IP=(.+)$', myArgv, re.IGNORECASE)
		myMME.mme_s11_IP = matchReg.group(1)
	elif re.match('^\-\-mme_s11_name=(.+)$', myArgv, re.IGNORECASE):
		matchReg = re.match('^\-\-mme_s11_name=(.+)$', myArgv, re.IGNORECASE)
		myMME.mme_s11_name = matchReg.group(1)
	elif re.match('^\-\-spgwc0_s11_IP=(.+)$', myArgv, re.IGNORECASE):
		matchReg = re.match('^\-\-spgwc0_s11_IP=(.+)$', myArgv, re.IGNORECASE)
		myMME.spgwc0_s11_IP = matchReg.group(1)
	elif re.match('^\-\-from_docker_file', myArgv, re.IGNORECASE):
		myMME.fromDockerFile = True
	else:
		Usage()
		sys.exit('Invalid Parameter: ' + myArgv)

if myMME.kind == '':
	Usage()
	sys.exit('missing kind parameter')

if myMME.kind == 'MME':
	if myMME.mme_s6a_IP == '':
		Usage()
		sys.exit('missing MME S6A IP address')
	elif myMME.hss_s6a_IP == '':
		Usage()
		sys.exit('missing HSS S6A IP address')
	elif myMME.mme_s1c_IP == '':
		Usage()
		sys.exit('missing MME S1-C IP address')
	elif myMME.mme_s1c_name == '':
		Usage()
		sys.exit('missing MME S1-C Interface name')
	elif myMME.mme_s10_IP == '':
		Usage()
		sys.exit('missing MME S10 IP address')
	elif myMME.mme_s10_name == '':
		Usage()
		sys.exit('missing MME S10 Interface name')
	elif myMME.mme_s11_IP == '':
		Usage()
		sys.exit('missing MME S11 IP address')
	elif myMME.mme_s11_name == '':
		Usage()
		sys.exit('missing MME S11 Interface name')
	elif myMME.spgwc0_s11_IP == '':
		Usage()
		sys.exit('missing SPGW-C0 IP address')
	else:
		myMME.GenerateMMEConfigurer()
		sys.exit(0)
else:
	Usage()
	sys.exit('unsupported kind parameter')
