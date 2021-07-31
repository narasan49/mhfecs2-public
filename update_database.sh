#!/bin/bash
# dir=/virtual/narasan/data
dir=../data
python3 manage.py regist_skillbase ${dir}/${1}/SkillBase.xml
python3 manage.py regist_teniskillbase ${dir}/${1}/TeniSkillBase.xml

python3 manage.py regist_wep ${dir}/${1}/Weapon.xml
python3 manage.py regist_model ${dir}/${1}/EquipHead.xml
python3 manage.py regist_model ${dir}/${1}/EquipBody.xml
python3 manage.py regist_model ${dir}/${1}/EquipArm.xml
python3 manage.py regist_model ${dir}/${1}/EquipWst.xml
python3 manage.py regist_model ${dir}/${1}/EquipLeg.xml
python3 manage.py regist_jewel ${dir}/${1}/Jewel.xml
python3 manage.py regist_cuff ${dir}/${1}/SkillCuff.xml

python3 manage.py regist_wepkind
python3 manage.py regist_tag

if [ $# -eq 2 ]; then
  python3 manage.py update_hist $1 $2
  exit 0
fi
python3 manage.py update_hist $1
