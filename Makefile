
LOGFILE=unity.log

UNITY=/Applications/Unity/Hub/Editor/2022.3.56f1/Unity.app/Contents/MacOS/Unity
FLAGS=-quit -batchmode -logfile ${LOGFILE}

UNITY_GAME=$(PWD)/unity-game

VERSION=0.1.0

GREEN=\033[1;32m
RED=\033[1;31m
NC=\033[0m

all: help


install.hf-repo: # Clone the repository of HF space
	git clone git@hf.co:spaces/Mistral-AI-Game-Jam/Team15 hf-repo

build.unity.requirements: # Check if Unity is installed
	@[ -f $(UNITY) ] || (printf "${RED}Unity is not installed${NC}\n" && exit 1)

build.unity: build.unity.requirements # Build the Unity project for WEBGL
	@printf "${GREEN}Building Unity project...${NC}\n"
	@$(UNITY) -projectPath $(UNITY_GAME) -executeMethod BuildScript.BuildWebGL $(FLAGS)
	@printf "${GREEN}Unity project built successfully${NC}\n"

deploy.unity: clean.hf-space # Deploy the Unity project to the HF space
	@printf "${GREEN}Deploying Unity project...${NC}\n"
	@cp -r $(UNITY_GAME)/Builds/WebGL/ $(PWD)/hf-repo
	cd hf-repo && git lfs install && git lfs track Build/* && git add . && git commit -m "Deploy Unity project $(VERSION)"
	cd hf-repo && git push origin main
	@printf "${GREEN}Unity project deployed successfully${NC}\n"

deploy-and-build.unity: build.unity deploy.unity # Build and deploy the Unity project

clean.hf-space: # Clean the HF space
	rm -rf hf-repo/Build hf-repo/TemplateData hf-repo/index.html hf-repo/logo.png

clean.unity.builds: # Clean the Unity builds folder
	rm -rf $(UNITY_GAME)/Builds

help: # Display available commands
	@printf "\033[1;34m==== Available make commands ====\033[0m\n"
	@printf "install.hf-repo\t\t\tClone the repository of HF space\n"
	@printf "build.unity.requirements\tCheck if Unity is installed\n"
	@printf "build.unity\t\t\tBuild the Unity project for WEBGL\n"
	@printf "deploy.unity\t\t\tDeploy the Unity project to the HF space\n"
	@printf "deploy-and-build.unity\t\tBuild and deploy the Unity project\n"
	@printf "clean.hf-space\t\t\tClean the HF space\n"
	@printf "clean.unity.builds\t\tClean the Unity builds folder\n"
	@printf "help\t\t\t\tDisplay available commands\n"
