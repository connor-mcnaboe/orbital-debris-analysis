import { Injectable } from '@angular/core';
import {Observable} from "rxjs";
import {HttpClient} from "@angular/common/http";
import {environment} from "../../environments/environment";

@Injectable({
  providedIn: 'root'
})
export class MissionService {

  constructor(private httpClient: HttpClient) { }

  postMissionDto(missionDto: MissionDto): Observable<any> {
    return this.httpClient.post(
          `${environment.apiUrl}/threat-report/`,
          missionDto
        )
  }
}

export interface MissionDto {
  apogee: number
  perigee: number
  threat_tolerance_km: number
}
