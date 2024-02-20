import { Injectable } from '@angular/core';
import {Observable} from "rxjs";
import {HttpClient} from "@angular/common/http";

@Injectable({
  providedIn: 'root'
})
export class MissionService {

  constructor(private httpClient: HttpClient) { }

  postMissionDto(missionDto: MissionDto): Observable<any> {
    return this.httpClient.post(
          `localhost:8000/threat-report/`,
          missionDto
        )
  }
}

export interface MissionDto {
  apogee: number
  perigee: number
  threat_tolerance_km: number
}
