import lib.angular.core as ngcore
from services import ProjectService

from lib.logger import Logger
logger = Logger(__name__)


@ngcore.component
class ProjectTreeComponent(ngcore.Component):

    class ComponentData:
        selector = 'ide-project-tree'
        templateUrl = "app/templates/ide/project-tree.component.html"
        directives = []
        services = {
            'projects':ProjectService
        }


    def __init__(self):
        super(ProjectTreeComponent,self).__init__()

    def open_project(self,project):
        self.services.projects.open_project(project['id'])