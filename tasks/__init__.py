#    Tektur Worker - Camuda eternal task executor for ETL processes 
#    Copyright (C) 2020  Alex Düsel, tekturcms@gmail.com

#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

from tasks.exist import exist_load
from tasks.aws import s3_list, s3_get, s3_put
from tasks.http import http_request
from tasks.mail import send_mail
from tasks.transform import transform_xml, batch_transform_xml, batch_tidy_html
from tasks.validate import batch_validate_xml, generate_schematron_xslt
from tasks.zip import file_unzip, file_zip
from tasks.pathio import make_path, move_folder, delete_path

    
