git clone https://github.com/BESSER-PEARL/BESSER.git
cd BESSER
git checkout development
cd ..
ren BESSER BESSER-code
mkdir besser
mkdir testsbesser
xcopy /E "BESSER-code\besser" ".\besser"
xcopy /E "BESSER-code\tests" ".\testsbesser"
