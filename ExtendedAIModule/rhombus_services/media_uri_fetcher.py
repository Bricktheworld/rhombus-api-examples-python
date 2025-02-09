###################################################################################
# Copyright (c) 2021 Rhombus Systems                                              #
#                                                                                 # 
# Permission is hereby granted, free of charge, to any person obtaining a copy    #
# of this software and associated documentation files (the "Software"), to deal   #
# in the Software without restriction, including without limitation the rights    #
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell       #
# copies of the Software, and to permit persons to whom the Software is           #
# furnished to do so, subject to the following conditions:                        #
#                                                                                 # 
# The above copyright notice and this permission notice shall be included in all  #
# copies or substantial portions of the Software.                                 #
#                                                                                 # 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR      #
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,        #
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE     #
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER          #
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,   #
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE   #
# SOFTWARE.                                                                       #
###################################################################################

# Import type hints
from typing import Tuple

# Import RhombusAPI to send requests to get the MediaURIs and generate a federated token
import RhombusAPI as rapi

# Import ConnectionType to get the correct connection URI
from helper_types.connection_type import ConnectionType


def fetch_federated_token(api_client: rapi.ApiClient) -> str:
    # Create a new instance of the ORG API to get the federated token
    org_api = rapi.OrgWebserviceApi(api_client=api_client)
    # Get the federated session token
    federated_token_request = rapi.OrgGenerateFederatedSessionTokenRequest(duration_sec=60 * 20)
    federated_token_response = org_api.generate_federated_session_token(body=federated_token_request)

    return federated_token_response.federated_session_token


def fetch_media_uris(api_client: rapi.ApiClient, camera_uuid: str, duration: int, connection_type: ConnectionType) -> \
        Tuple[str, str]:
    """Get the lan URI of the camera and generate a federatedToken to download the VOD
    
    :param api_client: The API Client for sending requests to Rhombus
    :param camera_uuid: The UUID of the camera to get info for
    :param duration: How long the federated token should last in seconds
    :param connection_type: Whether to use LAN or WAN for the connection, by default LAN and unless you are on a different connection, you should really just use LAN
    :return: Returns the lan URI of the vod and the generated federated token
    """

    # Create a new instance of the Camera API for us to use
    cam_api = rapi.CameraWebserviceApi(api_client=api_client)

    # Request from Rhombus the media URIs of our camera
    media_uri_request = rapi.CameraGetMediaUrisWSRequest(camera_uuid=camera_uuid)
    media_uris = cam_api.get_media_uris(body=media_uri_request)

    # Create a new instance of the ORG API to get the federated token
    org_api = rapi.OrgWebserviceApi(api_client=api_client)
    # Get the federated session token
    federated_token_request = rapi.OrgGenerateFederatedSessionTokenRequest(duration_sec=duration)
    federated_token_response = org_api.generate_federated_session_token(body=federated_token_request)

    # Return our data
    return media_uris.lan_vod_mpd_uris_templates[
               0] if connection_type == ConnectionType.LAN else media_uris.wan_vod_mpd_uri_template, federated_token_response.federated_session_token
